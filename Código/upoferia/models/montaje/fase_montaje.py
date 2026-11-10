from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FaseMontaje(models.Model):

    _name = "upoferia.fase_montaje"
    _description = "Fase de montaje"
    _rec_name = "sNombre"
    _order = "plan_montaje_id, iSecuencia, id"

    sNombre = fields.Char(
        string="Nombre",
        required=True,
        help="Identifica la fase dentro de su plan de montaje",
    )
    iSecuencia = fields.Integer(string="Secuencia", default=10)
    sDescripcion = fields.Text(string="Descripción")

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
            'UNIQUE(plan_montaje_id, "sNombre")',
            "Ya existe una fase con ese nombre en este plan.",
        ),
    ]

    @api.depends("plan_montaje_id.sNombre", "sNombre")
    def _compute_display_name(self):
        for record in self:
            record.display_name = "%s / %s" % (
                record.plan_montaje_id.sNombre or "",
                record.sNombre or "",
            )

    @api.constrains("sNombre")
    def _check_nombre(self):
        for record in self:
            if not record.sNombre.strip():
                raise ValidationError("El nombre de la fase no puede estar vacío.")
