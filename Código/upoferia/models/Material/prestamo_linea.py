from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PrestamoLinea(models.Model):

    _name = "upoferia.prestamo_linea"
    _description = "Línea de préstamo"

    cantidad = fields.Integer(
        string="Cantidad", default=1, help="Unidades prestadas del material"
    )
    cantidad_devuelta = fields.Integer(string="Cantidad devuelta", default=0)
    # atributo derivado: se calcula comparando la cantidad prestada con la devuelta
    estado_devolucion = fields.Selection(
        [
            ("pendiente", "Pendiente"),
            ("parcial", "Parcial"),
            ("completa", "Completa"),
        ],
        "Estado de devolución",
        compute="_compute_estado_devolucion",
        store=True,
    )

    # Relaciones
    prestamo_id = fields.Many2one(
        "upoferia.prestamo", string="Préstamo", required=True, ondelete="cascade"
    )
    material_id = fields.Many2one(
        "upoferia.material", string="Material", required=True, ondelete="restrict"
    )

    _sql_constraints = [
        (
            "prestamo_material_unique",
            "UNIQUE(prestamo_id, material_id)",
            "Ese material ya está en el préstamo.",
        ),
        (
            "cantidad_positiva",
            "CHECK(cantidad > 0)",
            "La cantidad debe ser mayor que cero.",
        ),
        (
            "devuelta_no_negativa",
            "CHECK(cantidad_devuelta >= 0)",
            "La cantidad devuelta no puede ser negativa.",
        ),
        (
            "devuelta_no_supera",
            "CHECK(cantidad_devuelta <= cantidad)",
            "No se pueden devolver más unidades de las prestadas.",
        ),
    ]

    @api.depends("prestamo_id.referencia", "material_id.nombre")
    def _compute_display_name(self):
        for record in self:
            record.display_name = "%s - %s" % (
                record.prestamo_id.referencia or "",
                record.material_id.nombre or "",
            )

    @api.depends("cantidad", "cantidad_devuelta")
    def _compute_estado_devolucion(self):
        for record in self:
            if record.cantidad_devuelta <= 0:
                record.estado_devolucion = "pendiente"
            elif record.cantidad_devuelta < record.cantidad:
                record.estado_devolucion = "parcial"
            else:
                record.estado_devolucion = "completa"

    @api.onchange("cantidad_devuelta", "cantidad")
    def onchange_cantidad_devuelta(self):
        if self.cantidad_devuelta > self.cantidad:
            return {
                "value": {"cantidad_devuelta": self.cantidad},
                "warning": {
                    "title": "Cantidad devuelta excesiva",
                    "message": "No se pueden devolver más unidades de las prestadas; se ha ajustado al máximo.",
                },
            }
