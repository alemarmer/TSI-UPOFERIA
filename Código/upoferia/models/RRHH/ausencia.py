# Autor: Juanjo (Personal - RRHH y Turnos)
from odoo import models, fields, api


class Ausencia(models.Model):

    _name = 'upoferia.ausencia'
    _description = 'Ausencia de un empleado'
    _rec_names_search = ['empleado_id']
    _order = 'fecha_desde desc'

    fecha_desde = fields.Date(string="Desde", required=True, default=fields.Date.context_today)
    fecha_hasta = fields.Date(string="Hasta")
    estado = fields.Selection([('pendiente', 'Pendiente'),
                               ('aprobada', 'Aprobada'),
                               ('rechazada', 'Rechazada'),],
                              'Estado', default='pendiente')
    motivo = fields.Text(string="Motivo")

    # Relaciones
    empleado_id = fields.Many2one('upoferia.empleado', string="Empleado", required=True, ondelete='cascade')

    # Calculados
    dias = fields.Integer(string="Días", compute='_compute_dias', store=True)

    _sql_constraints = [
        ('natural_unique', 'UNIQUE(empleado_id, fecha_desde)', 'Ese empleado ya tiene una ausencia que empieza ese día.'),
        ('fechas_check', 'CHECK(fecha_hasta IS NULL OR fecha_hasta >= fecha_desde)',
         'La fecha de fin de la ausencia no puede ser anterior a la de inicio.'),
    ]

    @api.depends('empleado_id.nombre', 'fecha_desde', 'fecha_hasta')
    def _compute_display_name(self):
        for record in self:
            record.display_name = '%s: %s → %s' % (record.empleado_id.nombre or '?', record.fecha_desde or '?',
                                                  record.fecha_hasta or 'sin fin')

    @api.depends('fecha_desde', 'fecha_hasta')
    def _compute_dias(self):
        for record in self:
            record.dias = ((record.fecha_hasta or record.fecha_desde) - record.fecha_desde).days + 1 if record.fecha_desde else 0

    # Validaciones
    @api.constrains('empleado_id', 'fecha_desde', 'fecha_hasta')
    def _check_solape(self):
        for record in self.filtered(lambda r: r.estado != 'rechazada'):
            fin = record.fecha_hasta or record.fecha_desde
            otras = self.search([('empleado_id', '=', record.empleado_id.id), ('id', '!=', record.id),
                                 ('estado', '!=', 'rechazada'), ('fecha_desde', '<=', fin)])
            for otra in otras:
                if (otra.fecha_hasta or otra.fecha_desde) >= record.fecha_desde:
                    raise models.ValidationError('La ausencia se solapa con otra del mismo empleado (%s).' % otra.display_name)

    @api.constrains('estado', 'motivo')
    def _check_motivo_rechazo(self):
        for record in self:
            if record.estado == 'rechazada' and not (record.motivo or '').strip():
                raise models.ValidationError('Una ausencia rechazada debe indicar el motivo del rechazo.')

    @api.constrains('empleado_id')
    def _check_empleado_activo(self):
        for record in self:
            if not record.empleado_id.activo:
                raise models.ValidationError('No se pueden registrar ausencias a un empleado de baja (%s).' % record.empleado_id.nombre)

    @api.constrains('fecha_desde', 'fecha_hasta')
    def _check_duracion_maxima(self):
        for record in self:
            if record.dias > 365:
                raise models.ValidationError('Una ausencia no puede durar más de un año.')

    @api.constrains('estado', 'empleado_id', 'fecha_desde', 'fecha_hasta')
    def _check_turnos_asignados(self):
        for record in self.filtered(lambda r: r.estado == 'aprobada'):
            turnos = self.env['upoferia.turno'].search([('empleado_ids', 'in', record.empleado_id.ids),
                                                        ('fecha', '>=', record.fecha_desde),
                                                        ('fecha', '<=', record.fecha_hasta or record.fecha_desde)])
            if turnos:
                raise models.ValidationError('No se puede aprobar: %s tiene turnos asignados en esas fechas (%s).'
                                      % (record.empleado_id.nombre, ', '.join(turnos.mapped('display_name'))))

    @api.onchange('fecha_desde')
    def onchange_fecha_desde(self):
        if self.fecha_desde and (not self.fecha_hasta or self.fecha_hasta < self.fecha_desde):
            self.fecha_hasta = self.fecha_desde

    @api.onchange('estado')
    def onchange_estado(self):
        if self.estado == 'rechazada' and not self.motivo:
            return {'warning': {'title': 'Falta el motivo', 'message': 'Indica el motivo del rechazo.'}}

    # Reglas de negocio (capa ORM)
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if 'estado' in fields_list:
            res['estado'] = 'pendiente'
        return res

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['estado'] = 'pendiente' if vals.get('estado') == 'aprobada' else vals.get('estado', 'pendiente')
            if vals.get('motivo'):
                vals['motivo'] = vals['motivo'].strip()
        return super().create(vals_list)

    def write(self, vals):
        if {'fecha_desde', 'fecha_hasta', 'empleado_id'} & set(vals):
            for record in self:
                if record.estado == 'aprobada':
                    raise models.UserError('No se pueden cambiar las fechas de una ausencia ya aprobada.')
        return super().write(vals)

    def unlink(self):
        hoy = fields.Date.context_today(self)
        for record in self:
            if record.estado == 'aprobada' and record.fecha_desde <= hoy:
                raise models.UserError('No se puede eliminar una ausencia aprobada que ya ha comenzado.')
        return super().unlink()

    def copy(self, default=None):
        default = dict(default or {})
        default.update({'estado': 'pendiente', 'fecha_desde': fields.Date.context_today(self), 'fecha_hasta': False})
        return super().copy(default)

    def action_aprobar(self):
        self.write({'estado': 'aprobada'})

    def action_rechazar(self):
        self.write({'estado': 'rechazada'})