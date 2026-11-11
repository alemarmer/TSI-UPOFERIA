# Autor: Juanjo (Personal - RRHH y Turnos)
from odoo import models, fields, api


class Certificacion(models.Model):

    _name = 'upoferia.rrhh.certificacion'
    _description = 'Certificación de un empleado'
    _rec_name = 'titulo'
    _order = 'fecha_expedicion desc'

    titulo = fields.Char(string="Título", size=100, required=True)
    fecha_expedicion = fields.Date(string="Fecha de expedición")

    # Relaciones
    empleado_id = fields.Many2one('upoferia.rrhh.empleado', string="Empleado", required=True, ondelete='cascade')

    _sql_constraints = [
        ('natural_unique', 'UNIQUE(empleado_id, titulo)', 'Ese empleado ya tiene una certificación con ese título.'),
    ]

    # Validaciones
    @api.constrains('titulo')
    def _check_titulo(self):
        for record in self:
            if not record.titulo.strip():
                raise models.ValidationError('El título de la certificación no puede estar vacío.')

    @api.constrains('fecha_expedicion')
    def _check_fecha_expedicion(self):
        hoy = fields.Date.context_today(self)
        for record in self:
            if record.fecha_expedicion and record.fecha_expedicion > hoy:
                raise models.ValidationError('La fecha de expedición (%s) no puede ser futura.' % record.fecha_expedicion)

    @api.constrains('fecha_expedicion')
    def _check_fecha_razonable(self):
        for record in self:
            if record.fecha_expedicion and record.fecha_expedicion.year < 1950:
                raise models.ValidationError('La fecha de expedición (%s) es anterior a 1950; revísala.' % record.fecha_expedicion)

    @api.constrains('empleado_id')
    def _check_empleado_activo(self):
        for record in self:
            if not record.empleado_id.activo:
                raise models.ValidationError('No se puede registrar una certificación a un empleado de baja.')

    @api.onchange('fecha_expedicion')
    def onchange_fecha_expedicion(self):
        if self.fecha_expedicion and self.fecha_expedicion > fields.Date.context_today(self):
            self.fecha_expedicion = fields.Date.context_today(self)
            return {
                'warning': {'title': 'Fecha futura', 'message': 'La fecha de expedición no puede ser futura; se ha puesto la de hoy.'}
            }

    @api.onchange('titulo')
    def onchange_titulo(self):
        if self.titulo:
            self.titulo = self.titulo.strip()

    # Reglas de negocio (capa ORM)
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if 'fecha_expedicion' in fields_list:
            res['fecha_expedicion'] = fields.Date.context_today(self)
        return res

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('titulo'):
                vals['titulo'] = vals['titulo'].strip()
            if not vals.get('fecha_expedicion'):
                vals['fecha_expedicion'] = fields.Date.context_today(self)
        return super().create(vals_list)

    def write(self, vals):
        if vals.get('titulo'):
            vals['titulo'] = vals['titulo'].strip()
        if 'empleado_id' in vals:
            raise models.UserError('Una certificación no se puede reasignar a otro empleado; crea una nueva.')
        return super().write(vals)

    def unlink(self):
        # El personal fijo de cocina debe conservar al menos una certificación
        for empleado in self.mapped('empleado_id'):
            if empleado.tipo_personal == 'fijo' and empleado.rol == 'cocina' and not (empleado.certificacion_ids - self):
                raise models.UserError('No se puede dejar a %s sin certificaciones: es obligatoria para el personal de cocina fijo.'
                                % empleado.nombre)
        return super().unlink()

    def copy_data(self, default=None):
        vals_list = super().copy_data(default=default)
        if 'titulo' not in (default or {}):
            for record, vals in zip(self, vals_list):
                vals['titulo'] = '%s (copia)' % record.titulo
        return vals_list