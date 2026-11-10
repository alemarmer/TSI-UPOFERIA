# Autor: Juanjo (Personal - RRHH y Turnos)
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

# Propuesta de cálculo para TA-20 (pendiente de validar por el equipo): días de salario por año trabajado
DIAS_INDEMNIZACION = {'procedente': 0, 'improcedente': 33, 'objetivo': 20, 'mutuo_acuerdo': 0, 'fin_contrato': 12}
HORAS_JORNADA = 8


class Despido(models.Model):

    _name = 'upoferia.despido'
    _description = 'Despido de un contrato laboral'
    _rec_names_search = ['empleado_id']
    _order = 'fecha_despido desc'

    motivo = fields.Text(string="Motivo")
    fecha_despido = fields.Date(string="Fecha del despido", default=fields.Date.context_today)
    tipo_despido = fields.Selection([('procedente', 'Procedente'),
                                     ('improcedente', 'Improcedente'),
                                     ('objetivo', 'Objetivo'),
                                     ('mutuo_acuerdo', 'Mutuo acuerdo'),
                                     ('fin_contrato', 'Fin de contrato'),],
                                    'Tipo de despido')

    # Relaciones (clave heredada del contrato: empleado + fecha de inicio del contrato)
    contrato_laboral_id = fields.Many2one('upoferia.contrato_laboral', string="Contrato laboral", required=True, ondelete='cascade')
    empleado_id = fields.Many2one('upoferia.empleado', string="Empleado", related='contrato_laboral_id.empleado_id', store=True)
    fecha_inicio_contrato_laboral = fields.Date(string="Inicio del contrato", related='contrato_laboral_id.fecha_inicio', store=True)
    fecha_fin_contrato_original = fields.Date(string="Fin previsto del contrato", readonly=True, copy=False,
                                              help="Fecha de fin que tenía el contrato antes del despido; "
                                                   "se restaura si se elimina el despido")

    # Calculados
    indemnizacion = fields.Float(string="Indemnización", digits=(10, 2), compute='_compute_indemnizacion',
                                 help="Cálculo provisional (TA-20): precio/hora × jornada × días por año × años trabajados")

    _sql_constraints = [
        ('contrato_unique', 'UNIQUE(contrato_laboral_id)', 'Ese contrato ya tiene un despido registrado (RN-67).'),
    ]

    @api.depends('empleado_id.nombre', 'fecha_despido')
    def _compute_display_name(self):
        for record in self:
            record.display_name = 'Despido de %s (%s)' % (record.empleado_id.nombre or '?', record.fecha_despido or 's/f')

    @api.depends('contrato_laboral_id.precio_hora', 'fecha_inicio_contrato_laboral', 'fecha_despido', 'tipo_despido')
    def _compute_indemnizacion(self):
        for record in self:
            if not (record.contrato_laboral_id and record.fecha_despido and record.tipo_despido and record.fecha_inicio_contrato_laboral):
                record.indemnizacion = 0.0
                continue
            anios = max((record.fecha_despido - record.fecha_inicio_contrato_laboral).days, 0) / 365.0
            salario_diario = record.contrato_laboral_id.precio_hora * HORAS_JORNADA
            record.indemnizacion = round(salario_diario * DIAS_INDEMNIZACION.get(record.tipo_despido, 0) * anios, 2)

    # Validaciones
    @api.constrains('fecha_despido', 'contrato_laboral_id')
    def _check_fecha_despido(self):
        for record in self:
            inicio = record.fecha_inicio_contrato_laboral
            if record.fecha_despido and inicio and record.fecha_despido < inicio:
                raise ValidationError('La fecha del despido (%s) no puede ser anterior al inicio del contrato (%s).'
                                      % (record.fecha_despido, inicio))

    @api.constrains('fecha_despido')
    def _check_fecha_no_futura(self):
        hoy = fields.Date.context_today(self)
        for record in self:
            if record.fecha_despido and record.fecha_despido > hoy:
                raise ValidationError('La fecha del despido no puede ser futura.')

    @api.constrains('motivo', 'tipo_despido')
    def _check_motivo(self):
        for record in self:
            if record.tipo_despido in ('procedente', 'improcedente', 'objetivo') and not (record.motivo or '').strip():
                raise ValidationError('Un despido de tipo «%s» debe indicar el motivo.'
                                      % dict(self._fields['tipo_despido'].selection).get(record.tipo_despido))

    @api.constrains('contrato_laboral_id', 'fecha_despido')
    def _check_contrato_vigente(self):
        for record in self:
            # Se compara con el fin ORIGINAL: el despido ya ha modificado contrato.fecha_fin
            fin = record.fecha_fin_contrato_original
            if fin and record.fecha_despido and record.fecha_despido > fin:
                raise ValidationError('El contrato ya había terminado el %s; no se puede despedir después.' % fin)

    @api.constrains('tipo_despido', 'fecha_despido')
    def _check_tipo_obligatorio(self):
        for record in self:
            if record.fecha_despido and not record.tipo_despido:
                raise ValidationError('Indica el tipo de despido.')

    @api.onchange('tipo_despido')
    def onchange_tipo_despido(self):
        if self.tipo_despido == 'improcedente':
            return {
                'warning': {
                    'title': 'Despido improcedente',
                    'message': 'Este tipo conlleva indemnización; revisa el importe calculado.'
                }
            }

    @api.onchange('fecha_despido', 'contrato_laboral_id')
    def onchange_fecha(self):
        inicio = self.contrato_laboral_id.fecha_inicio
        if self.fecha_despido and inicio and self.fecha_despido < inicio:
            return {
                'value': {'fecha_despido': fields.Date.context_today(self)},
                'warning': {'title': 'Fecha incorrecta', 'message': 'El despido no puede ser anterior al inicio del contrato.'}
            }

    # Reglas de negocio (capa ORM): el despido cierra el contrato
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if 'tipo_despido' in fields_list:
            res.setdefault('tipo_despido', 'procedente')
        return res

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('contrato_laboral_id'):
                contrato = self.env['upoferia.contrato_laboral'].browse(vals['contrato_laboral_id'])
                vals['fecha_fin_contrato_original'] = contrato.fecha_fin
        records = super().create(vals_list)
        records._aplicar_fin_contrato()
        return records

    def _aplicar_fin_contrato(self):
        """El contrato termina en la fecha del despido (o en su fin original si no hay fecha)."""
        for record in self:
            record.contrato_laboral_id.fecha_fin = record.fecha_despido or record.fecha_fin_contrato_original

    def write(self, vals):
        if 'contrato_laboral_id' in vals:
            raise UserError('No se puede cambiar el contrato de un despido.')
        res = super().write(vals)
        if 'fecha_despido' in vals:
            self._aplicar_fin_contrato()
        return res

    def unlink(self):
        for record in self:
            if record.fecha_despido and record.fecha_despido < fields.Date.context_today(self) and not self.env.su:
                raise UserError('No se puede eliminar un despido ya efectivo (%s).' % record.display_name)
        # Se restaura la fecha de fin que tenía el contrato antes del despido
        for record in self:
            record.contrato_laboral_id.fecha_fin = record.fecha_fin_contrato_original
        return super().unlink()

    def copy(self, default=None):
        raise UserError('No se puede duplicar un despido: cada contrato tiene como máximo uno (RN-67).')