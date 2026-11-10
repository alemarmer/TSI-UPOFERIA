# Autor: Juanjo (Personal - RRHH y Turnos)
from odoo import models, fields, api


class Empleado(models.Model):

    _name = 'upoferia.rrhh.empleado'
    _description = 'Empleado'
    _inherits = {'upoferia.socios.persona': 'persona_id'}
    _rec_name = 'nombre'
    _order = 'nombre'

    # La clave (dni) y los datos personales se heredan de Persona (especialización)
    persona_id = fields.Many2one('upoferia.socios.persona', string="Persona", required=True, ondelete='cascade')
    rol = fields.Selection([('encargado', 'Encargado de caseta'),
                            ('camarero', 'Camarero/a'),
                            ('cocina', 'Cocina'),
                            ('montaje', 'Montaje'),
                            ('limpieza', 'Limpieza'),
                            ('seguridad', 'Seguridad / Acceso'),
                            ('otro', 'Otro'),],
                           'Rol')
    puesto = fields.Char(string="Puesto", size=100)
    tipo_personal = fields.Selection([('fijo', 'Fijo'),
                                      ('temporal', 'Temporal'),
                                      ('voluntario', 'Voluntario'),
                                      ('colaborador', 'Colaborador externo'),],
                                     'Tipo de personal', default='temporal')
    activo = fields.Boolean(string="Activo", default=True)

    # Relaciones
    disponibilidad_ids = fields.One2many('upoferia.rrhh.disponibilidad', 'empleado_id', string="Disponibilidad")
    certificacion_ids = fields.One2many('upoferia.rrhh.certificacion', 'empleado_id', string="Certificaciones")
    ausencia_ids = fields.One2many('upoferia.rrhh.ausencia', 'empleado_id', string="Ausencias")
    contrato_laboral_ids = fields.One2many('upoferia.rrhh.contrato_laboral', 'empleado_id', string="Contratos laborales")
    entrega_uniforme_ids = fields.One2many('upoferia.rrhh.entrega_uniforme', 'empleado_id', string="Entregas de uniforme")
    asignacion_taquilla_ids = fields.One2many('upoferia.rrhh.asignacion_taquilla', 'empleado_id', string="Asignaciones de taquilla")
    formacion_ids = fields.One2many('upoferia.rrhh.formacion_empleado', 'empleado_id', string="Formación")
    turno_ids = fields.Many2many('upoferia.rrhh.turno', 'upoferia_rrhh_empleado_turno_rel', 'empleado_id', 'turno_id',
                              string="Turnos asignados")

    # Calculados
    taquilla_actual_id = fields.Many2one('upoferia.rrhh.taquilla', string="Taquilla actual", compute='_compute_taquilla_actual')
    num_turnos = fields.Integer(string="Nº de turnos", compute='_compute_num_turnos')

    _sql_constraints = [
        ('persona_unique', 'UNIQUE(persona_id)', 'Esa persona ya tiene el perfil de empleado.'),
    ]

    @api.depends('nombre', 'dni')
    def _compute_display_name(self):
        for record in self:
            record.display_name = '%s (%s)' % (record.nombre or '?', record.dni or '?')

    @api.depends('asignacion_taquilla_ids.fecha_fin')
    def _compute_taquilla_actual(self):
        for record in self:
            vigente = record.asignacion_taquilla_ids.filtered(lambda a: not a.fecha_fin)[:1]
            record.taquilla_actual_id = vigente.taquilla_id

    @api.depends('turno_ids')
    def _compute_num_turnos(self):
        for record in self:
            record.num_turnos = len(record.turno_ids)

    # Validaciones
    @api.constrains('puesto')
    def _check_puesto(self):
        for record in self:
            if record.puesto is not False and record.puesto and not record.puesto.strip():
                raise models.ValidationError('El puesto del empleado no puede contener solo espacios.')

    @api.constrains('disponibilidad_ids')
    def _check_disponibilidades(self):
        for record in self:
            if not record.disponibilidad_ids:
                raise models.ValidationError('El empleado %s debe tener al menos una franja de disponibilidad (RN-66).' % record.nombre)

    @api.constrains('tipo_personal', 'rol')
    def _check_rol_personal_fijo(self):
        for record in self:
            if record.tipo_personal == 'fijo' and not record.rol:
                raise models.ValidationError('El personal fijo debe tener un rol asignado.')

    @api.constrains('activo', 'turno_ids')
    def _check_archivar_con_turnos(self):
        hoy = fields.Date.context_today(self)
        for record in self:
            if not record.activo and record.turno_ids.filtered(lambda t: t.fecha >= hoy):
                raise models.ValidationError('No se puede dar de baja a %s: tiene turnos futuros asignados.' % record.nombre)

    @api.constrains('activo', 'contrato_laboral_ids')
    def _check_baja_con_contrato_vigente(self):
        hoy = fields.Date.context_today(self)
        for record in self:
            vigentes = record.contrato_laboral_ids.filtered(lambda c: not c.fecha_fin or c.fecha_fin > hoy)
            if not record.activo and vigentes:
                raise models.ValidationError('No se puede dar de baja a %s: tiene un contrato vigente. Registra antes el despido.'
                                      % record.nombre)

    @api.onchange('rol')
    def onchange_rol(self):
        if self.rol and not self.puesto:
            self.puesto = dict(self._fields['rol'].selection).get(self.rol)

    @api.onchange('tipo_personal')
    def onchange_tipo_personal(self):
        if self.tipo_personal == 'fijo' and not self.rol:
            return {
                'warning': {
                    'title': 'Falta el rol',
                    'message': 'El personal fijo necesita un rol asignado.'
                }
            }

    # Reglas de negocio (capa ORM)
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if 'activo' in fields_list:
            res['activo'] = True
        return res

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('puesto'):
                vals['puesto'] = vals['puesto'].strip()
            if not vals.get('puesto') and vals.get('rol'):
                vals['puesto'] = dict(self._fields['rol'].selection).get(vals['rol'])
        return super().create(vals_list)

    def write(self, vals):
        if 'persona_id' in vals:
            raise models.UserError('No se puede cambiar la persona de un empleado: crea un empleado nuevo.')
        if vals.get('puesto'):
            vals['puesto'] = vals['puesto'].strip()
        if vals.get('activo') is False:
            # Al darse de baja, se libera su taquilla
            for record in self:
                record.asignacion_taquilla_ids.filtered(lambda a: not a.fecha_fin).action_cerrar()
        return super().write(vals)

    def unlink(self):
        for record in self:
            if record.contrato_laboral_ids or record.ausencia_ids:
                raise models.UserError('No se puede eliminar a %s: tiene contratos o ausencias registrados. '
                                'Dalo de baja en su lugar.' % record.nombre)
        return super().unlink()

    def copy(self, default=None):
        raise models.UserError('No se puede duplicar un empleado: es único por su DNI.')

    def action_ver_turnos(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Turnos de %s' % self.nombre,
            'res_model': 'upoferia.rrhh.turno',
            'view_mode': 'calendar,list,form',
            'domain': [('empleado_ids', 'in', self.ids)],
        }