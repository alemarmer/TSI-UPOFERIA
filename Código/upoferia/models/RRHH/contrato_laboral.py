# Autor: Juanjo (Personal - RRHH y Turnos)
from odoo import models, fields, api
from datetime import timedelta


class ContratoLaboral(models.Model):

    _name = 'upoferia.rrhh.contrato_laboral'
    _description = 'Contrato laboral'
    _rec_names_search = ['empleado_id']
    _order = 'fecha_inicio desc'

    fecha_inicio = fields.Date(string="Fecha de inicio", required=True, default=fields.Date.context_today)
    fecha_fin = fields.Date(string="Fecha de fin")
    tipo_contrato = fields.Selection([('indefinido', 'Indefinido'),
                                      ('temporal', 'Temporal'),
                                      ('obra', 'Por obra o servicio'),
                                      ('fijo_discontinuo', 'Fijo discontinuo'),],
                                     'Tipo de contrato', default='temporal')
    precio_hora = fields.Float(string="Precio por hora", digits=(10, 2), help="Base del cálculo de la nómina (RN-20)")

    # Relaciones
    empleado_id = fields.Many2one('upoferia.rrhh.empleado', string="Empleado", required=True, ondelete='cascade')
    despido_ids = fields.One2many('upoferia.rrhh.despido', 'contrato_laboral_id', string="Despido")

    # Calculados
    tiene_despido = fields.Boolean(string="Con despido", compute='_compute_tiene_despido', store=True)
    vigente = fields.Boolean(string="Vigente", compute='_compute_vigente')

    _sql_constraints = [
        ('natural_unique', 'UNIQUE(empleado_id, fecha_inicio)', 'Ese empleado ya tiene un contrato que empieza ese día.'),
        ('fechas_check', 'CHECK(fecha_fin IS NULL OR fecha_fin >= fecha_inicio)',
         'La fecha de fin del contrato no puede ser anterior a la de inicio.'),
        ('precio_hora_check', 'CHECK(precio_hora IS NULL OR precio_hora >= 0)', 'El precio por hora no puede ser negativo.'),
    ]

    @api.depends('empleado_id.nombre', 'fecha_inicio')
    def _compute_display_name(self):
        for record in self:
            record.display_name = 'Contrato de %s (%s)' % (record.empleado_id.nombre or '?', record.fecha_inicio or '?')

    @api.depends('despido_ids')
    def _compute_tiene_despido(self):
        for record in self:
            record.tiene_despido = bool(record.despido_ids)

    def _compute_vigente(self):
        hoy = fields.Date.context_today(self)
        for record in self:
            record.vigente = record.fecha_inicio <= hoy and (not record.fecha_fin or record.fecha_fin >= hoy) if record.fecha_inicio else False

    # Validaciones
    @api.constrains('empleado_id', 'fecha_inicio', 'fecha_fin')
    def _check_solape_contratos(self):
        for record in self:
            otros = self.search([('empleado_id', '=', record.empleado_id.id), ('id', '!=', record.id)])
            for otro in otros:
                fin_a = record.fecha_fin or fields.Date.to_date('9999-12-31')
                fin_b = otro.fecha_fin or fields.Date.to_date('9999-12-31')
                if record.fecha_inicio <= fin_b and otro.fecha_inicio <= fin_a:
                    raise models.ValidationError('El contrato se solapa con otro del mismo empleado (%s).' % otro.display_name)

    @api.constrains('tipo_contrato', 'fecha_fin')
    def _check_fecha_fin_temporal(self):
        for record in self:
            if record.tipo_contrato in ('temporal', 'obra') and not record.fecha_fin and not record.despido_ids:
                raise models.ValidationError('Un contrato «%s» debe indicar la fecha de fin.'
                                      % dict(self._fields['tipo_contrato'].selection).get(record.tipo_contrato))

    @api.constrains('despido_ids')
    def _check_un_despido(self):
        for record in self:
            if len(record.despido_ids) > 1:
                raise models.ValidationError('Un contrato solo puede tener un despido (RN-67).')

    @api.constrains('precio_hora')
    def _check_precio_hora_maximo(self):
        for record in self:
            if record.precio_hora > 200:
                raise models.ValidationError('El precio por hora (%.2f) parece excesivo; revísalo.' % record.precio_hora)

    @api.constrains('empleado_id')
    def _check_empleado_activo(self):
        for record in self:
            if not record.empleado_id.activo:
                raise models.ValidationError('No se puede hacer un contrato a un empleado de baja (%s).' % record.empleado_id.nombre)

    @api.onchange('tipo_contrato', 'fecha_inicio')
    def onchange_tipo_contrato(self):
        if self.tipo_contrato == 'indefinido':
            self.fecha_fin = False
        elif self.tipo_contrato in ('temporal', 'obra') and self.fecha_inicio and not self.fecha_fin:
            self.fecha_fin = self.fecha_inicio + timedelta(days=90)

    @api.onchange('precio_hora')
    def onchange_precio_hora(self):
        if self.precio_hora and self.precio_hora < 0:
            self.precio_hora = abs(self.precio_hora)
            return {
                'warning': {'title': 'Precio negativo', 'message': 'El precio por hora se guarda siempre en positivo.'}
            }

    # Reglas de negocio (capa ORM)
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if 'precio_hora' in fields_list and not res.get('precio_hora') and res.get('empleado_id'):
            # Se propone el precio del último contrato del MISMO empleado
            ultimo = self.search([('empleado_id', '=', res['empleado_id']), ('precio_hora', '>', 0)],
                                 order='fecha_inicio desc', limit=1)
            res['precio_hora'] = ultimo.precio_hora or 0.0
        return res

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('tipo_contrato') == 'indefinido':
                vals['fecha_fin'] = False
            if vals.get('precio_hora'):
                vals['precio_hora'] = round(vals['precio_hora'], 2)
        return super().create(vals_list)

    def write(self, vals):
        if 'fecha_inicio' in vals or 'empleado_id' in vals:
            for record in self:
                if record.despido_ids:
                    raise models.UserError('No se puede cambiar el inicio ni el empleado de un contrato que tiene despido.')
        if vals.get('precio_hora'):
            vals['precio_hora'] = round(vals['precio_hora'], 2)
        return super().write(vals)

    def unlink(self):
        for record in self:
            if record.despido_ids:
                raise models.UserError('No se puede eliminar el contrato de %s: tiene un despido registrado.' % record.empleado_id.nombre)
        return super().unlink()

    def copy_data(self, default=None):
        # La copia es la renovación: empieza al día siguiente del fin y dura lo mismo que el original
        default = dict(default or {})
        vals_list = super().copy_data(default=default)
        hoy = fields.Date.context_today(self)
        for record, vals in zip(self, vals_list):
            if 'fecha_inicio' not in default:
                vals['fecha_inicio'] = (record.fecha_fin or hoy) + timedelta(days=1)
            if 'fecha_fin' not in default:
                duracion = record.fecha_fin - record.fecha_inicio if record.fecha_fin else None
                vals['fecha_fin'] = vals['fecha_inicio'] + duracion if duracion is not None else False
        return vals_list

    def action_registrar_despido(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Registrar despido',
            'res_model': 'upoferia.rrhh.despido',
            'view_mode': 'form',
            'context': {'default_contrato_laboral_id': self.id},
            'target': 'new',
        }