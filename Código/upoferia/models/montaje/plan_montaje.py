from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class PlanMontaje(models.Model):

    _name = "upoferia.plan_montaje"
    _description = "Plan de montaje"
    _rec_name = "nombre"

    nombre = fields.Char(
        string="Nombre", required=True, help="Identificador único del plan de montaje"
    )
    edicion = fields.Char(
        string="Edición", help="Edición de la feria, por ejemplo 2026"
    )
    fecha_inicio = fields.Date(string="Fecha de inicio")
    fecha_fin = fields.Date(string="Fecha de fin")
    estado = fields.Selection(
        [
            ("planificado", "Planificado"),
            ("en_curso", "En curso"),
            ("finalizado", "Finalizado"),
        ],
        "Estado",
        default="planificado",
    )
    responsable = fields.Char(string="Responsable")

    # Relaciones
    # PENDIENTE DE INTEGRAR CON INFRAESTRUCTURA (necesita upoferia.zona_caseta):
    # zona_caseta_id = fields.Many2one('upoferia.zona_caseta', string="Zona de caseta", ondelete='set null')
    fase_montaje_ids = fields.One2many(
        "upoferia.fase_montaje", "plan_montaje_id", string="Fases"
    )

    _sql_constraints = [
        (
            "nombre_unique",
            "UNIQUE(nombre)",
            "Ya existe un plan de montaje con ese nombre.",
        ),
        (
            "fechas_orden",
            "CHECK(fecha_fin >= fecha_inicio)",
            "La fecha de fin no puede ser anterior a la de inicio.",
        ),
    ]

    @api.constrains("nombre")
    def _check_nombre(self):
        for record in self:
            if not record.nombre.strip():
                raise ValidationError(
                    "El nombre del plan de montaje no puede estar vacío."
                )

    @api.onchange("fecha_inicio")
    def onchange_fecha_inicio(self):
        if self.fecha_inicio and not self.fecha_fin:
            self.fecha_fin = self.fecha_inicio + timedelta(days=7)
