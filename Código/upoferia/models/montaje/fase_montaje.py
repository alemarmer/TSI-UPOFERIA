from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FaseMontaje(models.Model):

    _name = "upoferia.fase_montaje"
    _description = "Fase de montaje"
    _rec_name = "nombre"
    _order = "plan_montaje_id, secuencia, id"

    nombre = fields.Char(
        string="Nombre",
        required=True,
        help="Identifica la fase dentro de su plan de montaje",
    )
    secuencia = fields.Integer(string="Secuencia", default=10)
    descripcion = fields.Text(string="Descripción")

    # Relaciones
    plan_montaje_id = fields.Many2one(
        "upoferia.plan_montaje",
        string="Plan de montaje",
        required=True,
        ondelete="cascade",
    )
    tarea_montaje_ids = fields.One2many(
        "upoferia.tarea_montaje", "fase_montaje_id", string="Tareas"
    )

    _sql_constraints = [
        (
            "nombre_plan_unique",
            "UNIQUE(plan_montaje_id, nombre)",
            "Ya existe una fase con ese nombre en este plan.",
        ),
    ]

    @api.depends("plan_montaje_id.nombre", "nombre")
    def _compute_display_name(self):
        for record in self:
            record.display_name = "%s / %s" % (
                record.plan_montaje_id.nombre or "",
                record.nombre or "",
            )

    @api.constrains("nombre")
    def _check_nombre(self):
        for record in self:
            if not record.nombre.strip():
                raise ValidationError("El nombre de la fase no puede estar vacío.")
