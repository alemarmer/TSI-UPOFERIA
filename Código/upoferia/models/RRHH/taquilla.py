# Autor: Juanjo (Personal - RRHH y Turnos)
from odoo import models, fields, api


class Taquilla(models.Model):

    _name = 'upoferia.taquilla'
    _description = 'Taquilla del personal'
    _rec_name = 'numero'
    _order = 'numero'

    numero = fields.Integer(string="Número", required=True, help="Número identificativo único de la taquilla")
    ubicacion = fields.Char(string="Ubicación", size=100)
    estado = fields.Selection([('disponible', 'Disponible'),
                               ('ocupada', 'Ocupada'),
                               ('mantenimiento', 'En mantenimiento'),],
                              'Estado', default='disponible')

    # Relaciones
    asignacion_ids = fields.One2many('upoferia.asignacion_taquilla', 'taquilla_id', string="Asignaciones")

    # Calculados
    asignacion_vigente_id = fields.Many2one('upoferia.asignacion_taquilla', string="Asignación vigente",
                                         compute='_compute_asignacion_vigente', store=True)
    empleado_actual_id = fields.Many2one('upoferia.empleado', string="Empleado actual",
                                      related='asignacion_vigente_id.empleado_id', store=True)
    num_asignaciones = fields.Integer(string="Nº de asignaciones", compute='_compute_num_asignaciones')

    _sql_constraints = [
        ('numero_unique', 'UNIQUE(numero)', 'Ya existe una taquilla con ese número.'),
        ('numero_positivo', 'CHECK(numero > 0)', 'El número de la taquilla debe ser mayor que 0.'),
    ]

    @api.depends('numero', 'ubicacion')
    def _compute_display_name(self):
        for record in self:
            record.display_name = 'Taquilla %s%s' % (record.numero, ' (%s)' % record.ubicacion if record.ubicacion else '')

    @api.depends('asignacion_ids.fecha_fin')
    def _compute_asignacion_vigente(self):
        for record in self:
            record.asignacion_vigente_id = record.asignacion_ids.filtered(lambda a: not a.fecha_fin)[:1]

    @api.depends('asignacion_ids')
    def _compute_num_asignaciones(self):
        for record in self:
            record.num_asignaciones = len(record.asignacion_ids)

    # Validaciones
    @api.constrains('numero')
    def _check_numero_maximo(self):
        for record in self:
            if record.numero > 999:
                raise models.ValidationError('El número de taquilla no puede superar 999.')

    @api.constrains('ubicacion')
    def _check_ubicacion(self):
        for record in self:
            if record.ubicacion and not record.ubicacion.strip():
                raise models.ValidationError('La ubicación de la taquilla no puede contener solo espacios.')

    @api.constrains('estado')
    def _check_estado(self):
        for record in self:
            vigentes = record.asignacion_ids.filtered(lambda a: not a.fecha_fin)
            if vigentes and record.estado != 'ocupada':
                raise models.ValidationError('La taquilla %s tiene una asignación vigente: debe estar «Ocupada».' % record.numero)
            if not vigentes and record.estado == 'ocupada':
                raise models.ValidationError('La taquilla %s no puede estar «Ocupada» sin una asignación vigente.' % record.numero)

    @api.onchange('estado')
    def onchange_estado(self):
        if self._origin.id and self.estado == 'mantenimiento' and self._origin.asignacion_vigente_id:
            return {
                'warning': {
                    'title': 'Taquilla asignada',
                    'message': 'La taquilla tiene una asignación vigente; ciérrala antes de ponerla en mantenimiento.'
                }
            }

    @api.onchange('numero')
    def onchange_numero(self):
        if self.numero and self.numero < 0:
            return {
                'value': {'numero': abs(self.numero)},
                'warning': {'title': 'Número negativo', 'message': 'El número de taquilla debe ser positivo; se ha corregido.'}
            }

    # Reglas de negocio (capa ORM)
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if 'numero' in fields_list:
            res['numero'] = (self.search([], order='numero desc', limit=1).numero or 0) + 1
        return res

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Una taquilla nueva nunca nace ocupada: solo la ocupa una asignación
            if vals.get('estado') == 'ocupada':
                vals['estado'] = 'disponible'
            if vals.get('ubicacion'):
                vals['ubicacion'] = vals['ubicacion'].strip()
        return super().create(vals_list)

    def write(self, vals):
        if vals.get('ubicacion'):
            vals['ubicacion'] = vals['ubicacion'].strip()
        if 'numero' in vals:
            for record in self:
                if record.asignacion_ids and vals['numero'] != record.numero:
                    raise models.UserError('No se puede renumerar la taquilla %s: ya tiene asignaciones registradas.' % record.numero)
        return super().write(vals)

    def unlink(self):
        for record in self:
            if record.asignacion_ids:
                raise models.UserError('No se puede eliminar la taquilla %s: tiene historial de asignaciones. '
                                'Ponla en mantenimiento en su lugar.' % record.numero)
        return super().unlink()

    def copy(self, default=None):
        default = dict(default or {})
        default['numero'] = (self.search([], order='numero desc', limit=1).numero or 0) + 1
        default['estado'] = 'disponible'
        return super().copy(default)

    def action_ver_asignaciones(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Asignaciones de la taquilla %s' % self.numero,
            'res_model': 'upoferia.asignacion_taquilla',
            'view_mode': 'list,form,calendar',
            'domain': [('taquilla_id', '=', self.id)],
            'context': {'default_taquilla_id': self.id},
        }

    def action_poner_mantenimiento(self):
        self.write({'estado': 'mantenimiento'})

    def action_poner_disponible(self):
        self.write({'estado': 'disponible'})