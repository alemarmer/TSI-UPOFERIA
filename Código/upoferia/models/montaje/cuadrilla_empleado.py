# PENDIENTE DE INTEGRAR CON RRHH: este modelo necesita upoferia.empleado, que es de otro.
# No se importa en montaje/__init__.py hasta que se integre (entonces se descomenta esa línea).

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CuadrillaEmpleado(models.Model):

    _name = "upoferia.cuadrilla_empleado"
    _description = "Miembro de cuadrilla"

    bEsJefe = fields.Boolean(
        string="Es jefe", default=False, help="Una cuadrilla solo puede tener un jefe"
    )

    # Relaciones
    cuadrilla_id = fields.Many2one(
        "upoferia.cuadrilla", string="Cuadrilla", required=True
    )
    empleado_id = fields.Many2one(
        "upoferia.empleado", string="Empleado", required=True
    )

    _sql_constraints = [
        (
            "miembro_unique",
            'UNIQUE(cuadrilla_id, empleado_id)',
            "Ese empleado ya pertenece a la cuadrilla.",
        ),
    ]

    @api.depends("cuadrilla_id.sNombre", "empleado_id.sNombre")
    def _compute_display_name(self):
        for record in self:
            record.display_name = "%s - %s" % (
                record.cuadrilla_id.sNombre or "",
                record.empleado_id.sNombre or "",
            )

    @api.constrains("bEsJefe", "cuadrilla_id")
    def _check_un_solo_jefe(self):
        for record in self:
            if record.bEsJefe and self.search_count(
                [
                    ("cuadrilla_id", "=", record.cuadrilla_id.id),
                    ("bEsJefe", "=", True),
                    ("id", "!=", record.id),
                ]
            ):
                raise ValidationError(
                    "La cuadrilla «%s» ya tiene un jefe." % record.cuadrilla_id.sNombre
                )

    @api.onchange("bEsJefe", "cuadrilla_id")
    def onchange_es_jefe(self):
        if (
            self.bEsJefe
            and self.cuadrilla_id
            and self.search_count(
                [
                    ("cuadrilla_id", "=", self.cuadrilla_id.id),
                    ("bEsJefe", "=", True),
                    ("id", "!=", self._origin.id),
                ]
            )
        ):
            return {
                "warning": {
                    "title": "La cuadrilla ya tiene jefe",
                    "message": "La cuadrilla «%s» ya tiene un jefe. Desmárcalo allí antes de nombrar otro."
                    % self.cuadrilla_id.sNombre,
                }
            }
