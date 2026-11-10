# Autor: Juanjo (Personal - RRHH y Turnos)
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class FormacionEmpleado(models.Model):

    _name = 'upoferia.formacion_empleado'
    _description = 'Formación realizada por un empleado'
    _rec_names_search = ['empleado_id', 'curso_formacion_id']

    nota = fields.Float(string="Nota", digits=(10, 2), help="Nota sobre 10")

    # Relaciones
    curso_formacion_id = fields.Many2one('upoferia.curso_formacion', string="Curso", required=True, ondelete='cascade')
    empleado_id = fields.Many2one('upoferia.empleado', string="Empleado", required=True, ondelete='cascade')

    # Calculados
    aprobado = fields.Boolean(string="Aprobado", compute='_compute_aprobado', store=True)

    _sql_constraints = [
        ('natural_unique', 'UNIQUE(curso_formacion_id, empleado_id)', 'Ese empleado ya está inscrito en el curso.'),
        ('nota_minima', 'CHECK(nota IS NULL OR nota >= 0)', 'La nota no puede ser negativa.'),
        ('nota_maxima', 'CHECK(nota IS NULL OR nota <= 10)', 'La nota no puede ser superior a 10.'),
    ]

    @api.depends('curso_formacion_id.nombre_curso', 'empleado_id.nombre')
    def _compute_display_name(self):
        for record in self:
            record.display_name = '%s – %s' % (record.empleado_id.nombre or '?', record.curso_formacion_id.nombre_curso or '?')

    @api.depends('nota')
    def _compute_aprobado(self):
        for record in self:
            record.aprobado = record.nota >= 5.0

    # Validaciones
    @api.constrains('empleado_id')
    def _check_empleado_activo(self):
        for record in self:
            if not record.empleado_id.activo:
                raise ValidationError('No se puede inscribir en un curso a un empleado de baja (%s).' % record.empleado_id.nombre)

    @api.constrains('nota', 'curso_formacion_id')
    def _check_nota_con_duracion(self):
        for record in self:
            if record.nota and not record.curso_formacion_id.duracion:
                raise ValidationError('No se puede poner nota en un curso sin duración definida (%s).'
                                      % record.curso_formacion_id.nombre_curso)

    @api.onchange('nota')
    def onchange_nota(self):
        if self.nota and (self.nota < 0 or self.nota > 10):
            return {
                'value': {'nota': max(0.0, min(10.0, self.nota))},
                'warning': {'title': 'Nota fuera de rango', 'message': 'La nota debe estar entre 0 y 10; se ha ajustado.'}
            }

    # Reglas de negocio (capa ORM)
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if 'nota' in fields_list:
            res['nota'] = 0.0
        return res

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('nota'):
                vals['nota'] = round(vals['nota'], 2)
        return super().create(vals_list)

    def write(self, vals):
        if 'curso_formacion_id' in vals or 'empleado_id' in vals:
            raise UserError('No se puede cambiar el curso ni el empleado de una inscripción; crea una nueva.')
        if vals.get('nota'):
            vals['nota'] = round(vals['nota'], 2)
        return super().write(vals)

    def unlink(self):
        for record in self:
            if record.nota:
                raise UserError('No se puede eliminar la inscripción de %s: ya tiene nota.' % record.display_name)
        return super().unlink()

    def copy(self, default=None):
        raise UserError('No se puede duplicar una inscripción: cada empleado solo se inscribe una vez por curso.')