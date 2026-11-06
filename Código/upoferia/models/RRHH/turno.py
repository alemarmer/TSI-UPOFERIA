from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta
import pytz

TZ_FERIA = pytz.timezone('Europe/Madrid')
MAX_HORAS_DIA = 12.0


def _float_a_datetime_utc(fecha, hora):
    """Convierte una fecha y una hora decimal (8.5 = 08:30) en un datetime UTC naive, tomando la hora como de Madrid."""
    local = TZ_FERIA.localize(datetime.combine(fecha, datetime.min.time()) + timedelta(hours=hora))
    return local.astimezone(pytz.utc).replace(tzinfo=None)


class Turno(models.Model):

    _name = 'upoferia.turno'
    _description = 'Turno de trabajo'
    _rec_names_search = ['empleado_ids']
    _order = 'fecha desc, hora_inicio'

    fecha = fields.Date(string="Fecha", required=True, default=fields.Date.context_today)
    hora_inicio = fields.Float(string="Hora de inicio", required=True, help="Hora en formato decimal (8.5 = 08:30)")
    hora_fin = fields.Float(string="Hora de fin", help="Hora en formato decimal (16.0 = 16:00)")

    # Relaciones
    empleado_ids = fields.Many2many('upoferia.empleado', 'upoferia_empleado_turno_rel', 'turno_id', 'empleado_id',
                                 string="Empleados asignados")

    # Calculados (usados por las vistas Calendar, Graph y Pivot)
    duracion = fields.Float(string="Duración (h)", compute='_compute_duracion', store=True)
    num_empleados = fields.Integer(string="Nº de empleados", compute='_compute_num_empleados', store=True)
    fecha_hora_inicio = fields.Datetime(string="Inicio", compute='_compute_fechas_hora', store=True)
    fecha_hora_fin = fields.Datetime(string="Fin", compute='_compute_fechas_hora', store=True)
    estado = fields.Selection([('pendiente', 'Pendiente'),
                               ('en_curso', 'En curso'),
                               ('finalizado', 'Finalizado'),],
                              'Estado', compute='_compute_estado')

    _sql_constraints = [
        ('natural_unique', 'UNIQUE(fecha, hora_inicio)', 'Ya existe un turno que empieza a esa hora en esa fecha.'),
        ('hora_inicio_rango', 'CHECK(hora_inicio >= 0 AND hora_inicio < 24)', 'La hora de inicio debe estar entre 00:00 y 23:59.'),
        ('hora_fin_rango', 'CHECK(hora_fin IS NULL OR hora_fin = 0 OR (hora_fin > 0 AND hora_fin <= 24))',
         'La hora de fin debe estar entre 00:00 y 24:00.'),
    ]

    @staticmethod
    def _formatea_hora(hora):
        horas, minutos = divmod(round((hora or 0.0) * 60), 60)
        return '%02d:%02d' % (horas, minutos)

    @api.depends('fecha', 'hora_inicio', 'hora_fin')
    def _compute_display_name(self):
        for record in self:
            if record.fecha:
                record.display_name = '%s  %s-%s' % (record.fecha.strftime('%d/%m/%Y'),
                                                     self._formatea_hora(record.hora_inicio),
                                                     self._formatea_hora(record.hora_fin) if record.hora_fin else '?')
            else:
                record.display_name = 'Turno nuevo'

    @api.depends('hora_inicio', 'hora_fin')
    def _compute_duracion(self):
        for record in self:
            record.duracion = max((record.hora_fin or record.hora_inicio) - record.hora_inicio, 0.0)

    @api.depends('empleado_ids')
    def _compute_num_empleados(self):
        for record in self:
            record.num_empleados = len(record.empleado_ids)

    @api.depends('fecha', 'hora_inicio', 'hora_fin')
    def _compute_fechas_hora(self):
        for record in self:
            if record.fecha:
                record.fecha_hora_inicio = _float_a_datetime_utc(record.fecha, record.hora_inicio)
                record.fecha_hora_fin = _float_a_datetime_utc(record.fecha, record.hora_fin or (record.hora_inicio + 1.0))
            else:
                record.fecha_hora_inicio = record.fecha_hora_fin = False

    def _compute_estado(self):
        ahora = fields.Datetime.now()
        for record in self:
            if not record.fecha_hora_inicio or ahora < record.fecha_hora_inicio:
                record.estado = 'pendiente'
            elif ahora <= record.fecha_hora_fin:
                record.estado = 'en_curso'
            else:
                record.estado = 'finalizado'

    # Validaciones
    @api.constrains('hora_inicio', 'hora_fin')
    def _check_horas(self):
        for record in self:
            if record.hora_fin and record.hora_fin <= record.hora_inicio:
                raise ValidationError('La hora de fin (%s) debe ser posterior a la de inicio (%s). '
                                      'Para turnos de noche, crea dos turnos (uno por día).'
                                      % (self._formatea_hora(record.hora_fin), self._formatea_hora(record.hora_inicio)))

    @api.constrains('empleado_ids', 'fecha', 'hora_inicio', 'hora_fin')
    def _check_solapamiento(self):
        for record in self:
            inicio, fin = record.hora_inicio, record.hora_fin or record.hora_inicio + 1.0
            otros = self.search([('fecha', '=', record.fecha), ('id', '!=', record.id),
                                 ('empleado_ids', 'in', record.empleado_ids.ids)])
            for otro in otros:
                if inicio < (otro.hora_fin or otro.hora_inicio + 1.0) and otro.hora_inicio < fin:
                    comunes = (record.empleado_ids & otro.empleado_ids).mapped('nombre')
                    raise ValidationError('%s ya está asignado al turno %s, que se solapa con este.'
                                          % (', '.join(comunes), otro.display_name))

    @api.constrains('empleado_ids', 'fecha')
    def _check_ausencias(self):
        for record in self.filtered('empleado_ids'):
            ausentes = self.env['upoferia.ausencia'].search([('empleado_id', 'in', record.empleado_ids.ids),
                                                             ('estado', '=', 'aprobada'),
                                                             ('fecha_desde', '<=', record.fecha),
                                                             '|', ('fecha_hasta', '>=', record.fecha),
                                                             '&', ('fecha_hasta', '=', False),
                                                             ('fecha_desde', '=', record.fecha)])
            if ausentes:
                raise ValidationError('Tienen una ausencia aprobada el %s: %s.'
                                      % (record.fecha, ', '.join(ausentes.mapped('empleado_id.nombre'))))

    @api.constrains('empleado_ids', 'fecha', 'hora_inicio', 'hora_fin')
    def _check_horas_diarias(self):
        for record in self:
            for empleado in record.empleado_ids:
                turnos = self.search([('fecha', '=', record.fecha), ('empleado_ids', 'in', empleado.id)])
                if sum(turnos.mapped('duracion')) > MAX_HORAS_DIA:
                    raise ValidationError('%s superaría las %d horas de trabajo el %s.'
                                          % (empleado.nombre, MAX_HORAS_DIA, record.fecha))

    @api.constrains('empleado_ids')
    def _check_empleados_activos(self):
        for record in self:
            de_baja = record.empleado_ids.filtered(lambda e: not e.activo)
            if de_baja:
                raise ValidationError('No se puede asignar a empleados de baja: %s.' % ', '.join(de_baja.mapped('nombre')))

    @api.onchange('hora_inicio')
    def onchange_hora_inicio(self):
        if self.hora_inicio and not self.hora_fin:
            self.hora_fin = min(self.hora_inicio + 8.0, 24.0)

    @api.onchange('empleado_ids', 'fecha')
    def onchange_empleados(self):
        if not self.fecha or not self.empleado_ids:
            return
        dia = str(self.fecha.weekday())
        sin_disponibilidad = self.empleado_ids.filtered(
            lambda e: e.disponibilidad_ids and dia not in e.disponibilidad_ids.mapped('dia_semana'))
        if sin_disponibilidad:
            return {
                'warning': {
                    'title': 'Fuera de disponibilidad',
                    'message': 'No han declarado disponibilidad para ese día de la semana: %s.'
                               % ', '.join(sin_disponibilidad.mapped('nombre'))
                }
            }

    # Reglas de negocio (capa ORM)
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if 'hora_inicio' in fields_list and not res.get('hora_inicio'):
            res['hora_inicio'] = 12.0
            res['hora_fin'] = 20.0
        return res

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('hora_inicio') is not None and not vals.get('hora_fin'):
                vals['hora_fin'] = min(vals['hora_inicio'] + 8.0, 24.0)
        return super().create(vals_list)

    def write(self, vals):
        hoy = fields.Date.context_today(self)
        if {'fecha', 'hora_inicio', 'hora_fin'} & set(vals):
            for record in self:
                if record.fecha < hoy:
                    raise UserError('No se puede modificar el horario de un turno ya pasado (%s).' % record.display_name)
        return super().write(vals)

    def unlink(self):
        hoy = fields.Date.context_today(self)
        for record in self:
            if record.fecha < hoy and record.empleado_ids:
                raise UserError('No se puede eliminar el turno %s: ya ha tenido lugar y tiene empleados asignados.'
                                % record.display_name)
        return super().unlink()

    def copy(self, default=None):
        default = dict(default or {})
        default['fecha'] = self.fecha + timedelta(days=1)
        default['empleado_ids'] = [(5, 0, 0)]
        return super().copy(default)

    def action_copiar_semana_siguiente(self):
        nuevos = self.env['upoferia.turno']
        for record in self:
            nuevos |= record.copy({'fecha': record.fecha + timedelta(days=7), 'empleado_ids': [(6, 0, record.empleado_ids.ids)]})
        return {
            'type': 'ir.actions.act_window',
            'name': 'Turnos copiados',
            'res_model': 'upoferia.turno',
            'view_mode': 'list,form,calendar',
            'domain': [('id', 'in', nuevos.ids)],
        }