from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class AsignacionTaquilla(models.Model):

    _name = 'upoferia.asignacion_taquilla'
    _description = 'Asignación de taquilla a un empleado'
    _rec_names_search = ['empleado_id', 'taquilla_id']
    _order = 'fecha_inicio desc'

    fecha_inicio = fields.Date(string="Fecha de inicio", required=True, default=fields.Date.context_today)
    fecha_fin = fields.Date(string="Fecha de fin", help="Vacía mientras la asignación esté vigente")

    # Relaciones
    taquilla_id = fields.Many2one('upoferia.taquilla', string="Taquilla", required=True, ondelete='cascade')
    empleado_id = fields.Many2one('upoferia.empleado', string="Empleado", required=True, ondelete='restrict')

    # Calculados
    vigente = fields.Boolean(string="Vigente", compute='_compute_vigente', store=True)
    duracion_dias = fields.Integer(string="Duración (días)", compute='_compute_duracion_dias')

    _sql_constraints = [
        ('natural_unique', 'UNIQUE(taquilla_id, fecha_inicio)', 'Esa taquilla ya tiene una asignación con esa fecha de inicio.'),
        ('fechas_check', 'CHECK(fecha_fin IS NULL OR fecha_fin >= fecha_inicio)',
         'La fecha de fin no puede ser anterior a la de inicio (RN-48).'),
    ]

    @api.depends('taquilla_id.numero', 'empleado_id.nombre', 'fecha_inicio')
    def _compute_display_name(self):
        for record in self:
            record.display_name = 'Taquilla %s → %s (%s)' % (record.taquilla_id.numero or '?', record.empleado_id.nombre or '?',
                                                           record.fecha_inicio or '')

    @api.depends('fecha_fin')
    def _compute_vigente(self):
        for record in self:
            record.vigente = not record.fecha_fin

    @api.depends('fecha_inicio', 'fecha_fin')
    def _compute_duracion_dias(self):
        hoy = fields.Date.context_today(self)
        for record in self:
            record.duracion_dias = max(((record.fecha_fin or hoy) - record.fecha_inicio).days, 0) if record.fecha_inicio else 0

    # Validaciones
    @api.constrains('taquilla_id', 'fecha_fin')
    def _check_taquilla_vigente_unica(self):
        for record in self.filtered(lambda r: not r.fecha_fin):
            if self.search_count([('taquilla_id', '=', record.taquilla_id.id), ('fecha_fin', '=', False), ('id', '!=', record.id)]):
                raise ValidationError('La taquilla %s ya tiene una asignación vigente (RN-48).' % record.taquilla_id.numero)

    @api.constrains('empleado_id', 'fecha_fin')
    def _check_empleado_vigente_unica(self):
        for record in self.filtered(lambda r: not r.fecha_fin):
            if self.search_count([('empleado_id', '=', record.empleado_id.id), ('fecha_fin', '=', False), ('id', '!=', record.id)]):
                raise ValidationError('%s ya tiene una taquilla asignada y vigente (RN-48).' % record.empleado_id.nombre)

    @api.constrains('taquilla_id', 'fecha_fin')
    def _check_taquilla_operativa(self):
        for record in self.filtered(lambda r: not r.fecha_fin):
            if record.taquilla_id.estado == 'mantenimiento':
                raise ValidationError('La taquilla %s está en mantenimiento y no se puede asignar.' % record.taquilla_id.numero)

    @api.constrains('empleado_id')
    def _check_empleado_activo(self):
        for record in self:
            if not record.empleado_id.activo:
                raise ValidationError('No se puede asignar una taquilla a un empleado de baja (%s).' % record.empleado_id.nombre)

    @api.constrains('fecha_inicio')
    def _check_fecha_inicio(self):
        hoy = fields.Date.context_today(self)
        for record in self:
            if record.fecha_inicio > hoy:
                raise ValidationError('La fecha de inicio de la asignación no puede ser futura.')

    @api.onchange('taquilla_id')
    def onchange_taquilla(self):
        if self.taquilla_id and self.taquilla_id.estado != 'disponible':
            return {
                'warning': {
                    'title': 'Taquilla no disponible',
                    'message': 'La taquilla %s está «%s».' % (
                        self.taquilla_id.numero, dict(self.taquilla_id._fields['estado'].selection).get(self.taquilla_id.estado))
                }
            }

    @api.onchange('empleado_id')
    def onchange_empleado(self):
        if self.empleado_id:
            vigente = self.search([('empleado_id', '=', self.empleado_id.id), ('fecha_fin', '=', False)], limit=1)
            if vigente and vigente != self._origin:
                return {
                    'warning': {
                        'title': 'Empleado con taquilla',
                        'message': '%s ya tiene la taquilla %s asignada.' % (self.empleado_id.nombre, vigente.taquilla_id.numero)
                    }
                }

    # Reglas de negocio (capa ORM): el estado de la taquilla sigue a sus asignaciones
    def _sincronizar_estado_taquillas(self, taquillas):
        for taquilla in taquillas.exists():
            if taquilla.estado == 'mantenimiento':
                continue
            nuevo = 'ocupada' if self.search_count([('taquilla_id', '=', taquilla.id), ('fecha_fin', '=', False)]) else 'disponible'
            if taquilla.estado != nuevo:
                taquilla.estado = nuevo

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if 'taquilla_id' in fields_list and not res.get('taquilla_id'):
            libre = self.env['upoferia.taquilla'].search([('estado', '=', 'disponible')], limit=1)
            if libre:
                res['taquilla_id'] = libre.id
        return res

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        self._sincronizar_estado_taquillas(records.mapped('taquilla_id'))
        return records

    def write(self, vals):
        if 'empleado_id' in vals:
            for record in self:
                if record.empleado_id.id != vals['empleado_id'] and record.fecha_fin:
                    raise UserError('No se puede cambiar el empleado de una asignación cerrada.')
        taquillas = self.mapped('taquilla_id')
        res = super().write(vals)
        self._sincronizar_estado_taquillas(taquillas | self.mapped('taquilla_id'))
        return res

    def unlink(self):
        taquillas = self.mapped('taquilla_id')
        res = super().unlink()
        self._sincronizar_estado_taquillas(taquillas)
        return res

    def copy(self, default=None):
        default = dict(default or {})
        default['fecha_inicio'] = fields.Date.context_today(self)
        default['fecha_fin'] = False
        return super().copy(default)

    def action_cerrar(self):
        hoy = fields.Date.context_today(self)
        for record in self:
            record.fecha_fin = max(hoy, record.fecha_inicio)