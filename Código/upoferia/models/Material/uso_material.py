from odoo import models, fields, api
from odoo.exceptions import ValidationError


class UsoMaterial(models.Model):

    _name = "upoferia.uso_material"
    _description = "Uso de material en una tarea"

    iCantidad = fields.Integer(
        string="Cantidad", default=1, help="Unidades del material que usa la tarea"
    )
    sObservaciones = fields.Text(string="Observaciones")

    # Relaciones
    material_id = fields.Many2one(
        "upoferia.material", string="Material", required=True, ondelete="cascade"
    )
    tarea_montaje_id = fields.Many2one(
        "upoferia.tarea_montaje",
        string="Tarea de montaje",
        required=True,
        ondelete="cascade",
    )
    plan_montaje_id = fields.Many2one(
        related="tarea_montaje_id.plan_montaje_id", string="Plan de montaje", store=True
    )

    _sql_constraints = [
        (
            "material_tarea_unique",
            'UNIQUE(material_id, tarea_montaje_id)',
            "Ese material ya está asignado a la tarea.",
        ),
        (
            "cantidad_positiva",
            'CHECK("iCantidad" > 0)',
            "La cantidad debe ser mayor que cero.",
        ),
    ]

    @api.depends("material_id.sNombre", "tarea_montaje_id.sNombre")
    def _compute_display_name(self):
        for record in self:
            record.display_name = "%s - %s" % (
                record.material_id.sNombre or "",
                record.tarea_montaje_id.sNombre or "",
            )

    @api.onchange("iCantidad", "material_id")
    def onchange_cantidad(self):
        if self.material_id and self.iCantidad > self.material_id.iCantidadTotal:
            return {
                "warning": {
                    "title": "Cantidad superior al total",
                    "message": "Pides %s unidades y de «%s» solo hay %s."
                    % (
                        self.iCantidad,
                        self.material_id.sNombre,
                        self.material_id.iCantidadTotal,
                    ),
                }
            }
