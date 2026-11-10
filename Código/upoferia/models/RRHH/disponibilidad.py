# Autor: Juanjo (Personal - RRHH y Turnos)
from odoo import models, fields, api

DIAS_SEMANA = [('0', 'Lunes'), ('1', 'Martes'), ('2', 'Miércoles'), ('3', 'Jueves'),
               ('4', 'Viernes'), ('5', 'Sábado'), ('6', 'Domingo')]


class Disponibilidad(models.Model):

    _name = 'upoferia.rrhh.disponibilidad'
    _description = 'Franja semanal de disponibilidad de un empleado'
    _rec_names_search = ['empleado_id']
    _order = 'empleado_id, dia_semana, hora_inicio'

    dia_semana = fields.Selection(DIAS_SEMANA, 'Día de la semana', required=True)
    fecha_fin = fields.Date(string="Fecha de fin", required=True, help="Fecha hasta la que es válida esta franja")
    hora_inicio = fields.Float(string="Hora de inicio", default=8.0, help="Hora en formato decimal (8.5 = 08:30)")

    # Relaciones
    empleado_id = fields.Many2one('upoferia.rrhh.empleado', string="Empleado", required=True, ondelete='cascade')

    _sql_constraints = [
        ('natural_unique', 'UNIQUE(empleado_id, dia_semana, fecha_fin)',
         'Ese empleado ya tiene una franja ese día de la semana con esa fecha de fin.'),
        ('hora_inicio_rango', 'CHECK(hora_inicio IS NULL OR (hora_inicio >= 0 AND hora_inicio < 24))',
         'La hora de inicio debe estar entre 00:00 y 23:59.'),
    ]

    @api.depends('empleado_id.nombre', 'dia_semana', 'hora_inicio')
    def _compute_display_name(self):
        dias = dict(DIAS_SEMANA)
        for record in self:
            record.display_name = '%s – %s desde las %02d:%02d' % (
                record.empleado_id.nombre or '?', dias.get(record.dia_semana, '?'),
                int(record.hora_inicio), round((record.hora_inicio % 1) * 60))

    # Validaciones
    @api.constrains('fecha_fin')
    def _check_fecha_fin(self):
        hoy = fields.Date.context_today(self)
        for record in self:
            if record.fecha_fin < hoy and not self.env.context.get('importando_historico'):
                raise models.ValidationError('La franja no puede terminar en el pasado (%s).' % record.fecha_fin)

    @api.constrains('hora_inicio')
    def _check_hora_cuartos(self):
        for record in self:
            if round(record.hora_inicio * 60) % 15:
                raise models.ValidationError('La hora de inicio debe ser múltiplo de 15 minutos.')

    @api.constrains('empleado_id')
    def _check_empleado_activo(self):
        for record in self:
            if not record.empleado_id.activo:
                raise models.ValidationError('No se puede registrar disponibilidad a un empleado de baja (%s).' % record.empleado_id.nombre)

    @api.onchange('hora_inicio')
    def onchange_hora_inicio(self):
        if self.hora_inicio and (self.hora_inicio < 0 or self.hora_inicio >= 24):
            self.hora_inicio = 8.0
            return {
                'warning': {'title': 'Hora incorrecta', 'message': 'La hora debe estar entre 00:00 y 23:59; se ha puesto 08:00.'}
            }

    # Reglas de negocio (capa ORM)
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if 'fecha_fin' in fields_list and not res.get('fecha_fin'):
            res['fecha_fin'] = fields.Date.context_today(self).replace(month=12, day=31)
        return res

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('hora_inicio') is not None:
                vals['hora_inicio'] = round(vals['hora_inicio'] * 4) / 4  # redondeo a cuartos de hora
        return super().create(vals_list)

    def write(self, vals):
        if 'empleado_id' in vals:
            raise models.UserError('No se puede mover una franja a otro empleado; crea una nueva.')
        if vals.get('hora_inicio') is not None:
            vals['hora_inicio'] = round(vals['hora_inicio'] * 4) / 4
        return super().write(vals)

    def unlink(self):
        if not self.env.context.get('force_unlink'):
            # Se comprueba por empleado y con todo el conjunto a borrar, para que no se puedan borrar todas de golpe
            for empleado in self.mapped('empleado_id'):
                if not (empleado.disponibilidad_ids - self):
                    raise models.ValidationError('%s debe conservar al menos una franja de disponibilidad (RN-66).' % empleado.nombre)
        return super().unlink()

    def copy_data(self, default=None):
        vals_list = super().copy_data(default=default)
        if 'dia_semana' not in (default or {}):
            for record, vals in zip(self, vals_list):
                vals['dia_semana'] = str((int(record.dia_semana) + 1) % 7)
        return vals_list