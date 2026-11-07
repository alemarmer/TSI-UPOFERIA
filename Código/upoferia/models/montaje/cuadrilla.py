from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Cuadrilla(models.Model):

    _name = "upoferia.cuadrilla"
    _description = "Cuadrilla de montaje"
    _rec_name = "nombre"

    nombre = fields.Char(
        string="Nombre", required=True, help="Identificador único de la cuadrilla"
    )
    especialidad = fields.Char(string="Especialidad")
    activa = fields.Boolean(string="Activa", default=True)

    # Relaciones
    cuadrilla_empleado_ids = fields.One2many(
        "upoferia.cuadrilla_empleado", "cuadrilla_id", string="Miembros"
    )
    tarea_montaje_ids = fields.One2many(
        "upoferia.tarea_montaje", "cuadrilla_id", string="Tareas de montaje"
    )

    _sql_constraints = [
        ("nombre_unique", "UNIQUE(nombre)", "Ya existe una cuadrilla con ese nombre."),
    ]

    @api.constrains("nombre")
    def _check_nombre(self):
        for record in self:
            if not record.nombre.strip():
                raise ValidationError("El nombre de la cuadrilla no puede estar vacío.")
