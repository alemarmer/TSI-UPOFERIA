from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class PlanMontaje(models.Model):

    _name = "upoferia.plan_montaje"
    _description = "Plan de montaje"
    _rec_name = "sNombre"

    sNombre = fields.Char(
        string="Nombre", required=True, help="Identificador único del plan de montaje"
    )
    sEdicion = fields.Char(
        string="Edición", help="Edición de la feria, por ejemplo 2026"
    )
    dFechaInicio = fields.Date(string="Fecha de inicio")
    dFechaFin = fields.Date(string="Fecha de fin")
    selEstado = fields.Selection(
        [
            ("planificado", "Planificado"),
            ("en_curso", "En curso"),
            ("finalizado", "Finalizado"),
        ],
        "Estado",
        default="planificado",
    )
    sResponsable = fields.Char(string="Responsable")

    # Relaciones
    # PENDIENTE DE INTEGRAR CON INFRAESTRUCTURA (necesita upoferia.zona_caseta):
    # zona_caseta_id = fields.Many2one('upoferia.zona_caseta', string="Zona de caseta")
    fase_montaje_ids = fields.One2many(
        "upoferia.fase_montaje", "plan_montaje_id", string="Fases"
    )

    _sql_constraints = [
        (
            "nombre_unique",
            'UNIQUE("sNombre")',
            "Ya existe un plan de montaje con ese nombre.",
        ),
    ]

    @api.constrains("sNombre")
    def _check_nombre(self):
        for record in self:
            if not record.sNombre.strip():
                raise ValidationError(
                    "El nombre del plan de montaje no puede estar vacío."
                )

    @api.constrains("dFechaInicio", "dFechaFin")
    def _check_fechas(self):
        for record in self:
            if record.dFechaInicio and record.dFechaFin and record.dFechaFin < record.dFechaInicio:
                raise ValidationError(
                    "La fecha de fin no puede ser anterior a la de inicio."
                )

    @api.onchange("dFechaInicio")
    def onchange_fecha_inicio(self):
        if self.dFechaInicio and not self.dFechaFin:
            self.dFechaFin = self.dFechaInicio + timedelta(days=7)
