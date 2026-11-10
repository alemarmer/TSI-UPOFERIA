# Autor: Juanjo (Personal - RRHH y Turnos)
from odoo import models, fields, api


class CursoFormacion(models.Model):

    _name = 'upoferia.rrhh.curso_formacion'
    _description = 'Curso de formación'
    _rec_name = 'nombre_curso'
    _order = 'nombre_curso'

    nombre_curso = fields.Char(string="Nombre del curso", size=100, required=True, help="Identificador único del curso")
    duracion = fields.Integer(string="Duración (horas)")
    formador = fields.Char(string="Formador", size=100)

    # Relaciones
    formacion_ids = fields.One2many('upoferia.rrhh.formacion_empleado', 'curso_formacion_id', string="Participantes")

    # Calculados
    num_participantes = fields.Integer(string="Nº de participantes", compute='_compute_estadisticas', store=True)
    nota_media = fields.Float(string="Nota media", compute='_compute_estadisticas', store=True, digits=(10, 2))

    _sql_constraints = [
        ('nombre_unique', 'UNIQUE(nombre_curso)', 'Ya existe un curso con ese nombre.'),
        ('duracion_positiva', 'CHECK(duracion IS NULL OR duracion >= 0)', 'La duración del curso no puede ser negativa.'),
    ]

    @api.depends('formacion_ids', 'formacion_ids.nota')
    def _compute_estadisticas(self):
        for record in self:
            notas = record.formacion_ids.filtered(lambda f: f.nota).mapped('nota')
            record.num_participantes = len(record.formacion_ids)
            record.nota_media = sum(notas) / len(notas) if notas else 0.0

    # Validaciones
    @api.constrains('nombre_curso')
    def _check_nombre(self):
        for record in self:
            if not record.nombre_curso.strip():
                raise models.ValidationError('El nombre del curso no puede estar vacío.')

    @api.constrains('duracion')
    def _check_duracion(self):
        for record in self:
            if record.duracion and record.duracion > 500:
                raise models.ValidationError('Un curso de %d horas no es razonable; revisa la duración (máx. 500 h).' % record.duracion)

    @api.constrains('formador')
    def _check_formador(self):
        for record in self:
            if record.formador and not any(c.isalpha() for c in record.formador):
                raise models.ValidationError('El nombre del formador debe contener letras.')

    @api.constrains('formacion_ids')
    def _check_aforo(self):
        for record in self:
            if len(record.formacion_ids) > 50:
                raise models.ValidationError('El curso «%s» no puede tener más de 50 participantes.' % record.nombre_curso)

    @api.onchange('duracion')
    def onchange_duracion(self):
        if self.duracion and self.duracion < 0:
            self.duracion = abs(self.duracion)
            return {
                'warning': {'title': 'Duración negativa', 'message': 'La duración se guarda siempre en positivo.'}
            }

    @api.onchange('nombre_curso')
    def onchange_nombre(self):
        if self.nombre_curso:
            self.nombre_curso = self.nombre_curso.strip()

    # Reglas de negocio (capa ORM)
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if 'duracion' in fields_list:
            res['duracion'] = 8
        return res

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('nombre_curso'):
                vals['nombre_curso'] = vals['nombre_curso'].strip()
            if vals.get('formador'):
                vals['formador'] = vals['formador'].strip().title()
        return super().create(vals_list)

    def write(self, vals):
        if vals.get('nombre_curso'):
            vals['nombre_curso'] = vals['nombre_curso'].strip()
        if vals.get('formador'):
            vals['formador'] = vals['formador'].strip().title()
        if 'duracion' in vals:
            for record in self:
                if record.num_participantes and vals['duracion'] != record.duracion:
                    raise models.UserError('No se puede cambiar la duración de «%s»: ya tiene %d participantes.'
                                    % (record.nombre_curso, record.num_participantes))
        return super().write(vals)

    def unlink(self):
        for record in self:
            if record.formacion_ids.filtered('nota'):
                raise models.UserError('No se puede eliminar el curso «%s»: hay empleados con nota registrada.' % record.nombre_curso)
        return super().unlink()

    def copy_data(self, default=None):
        vals_list = super().copy_data(default=default)
        if 'nombre_curso' not in (default or {}):
            for record, vals in zip(self, vals_list):
                vals['nombre_curso'] = '%s (copia)' % record.nombre_curso
        return vals_list