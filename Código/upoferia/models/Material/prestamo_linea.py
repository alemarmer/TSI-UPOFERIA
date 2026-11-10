from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PrestamoLinea(models.Model):

    _name = "upoferia.prestamo_linea"
    _description = "Línea de préstamo"

    iCantidad = fields.Integer(
        string="Cantidad", default=1, help="Unidades prestadas del material"
    )
    iCantidadDevuelta = fields.Integer(string="Cantidad devuelta", default=0)
    # atributo derivado: se calcula comparando la cantidad prestada con la devuelta
    selEstadoDevolucion = fields.Selection(
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
            'UNIQUE(prestamo_id, material_id)',
            "Ese material ya está en el préstamo.",
        ),
        (
            "cantidad_positiva",
            'CHECK("iCantidad" > 0)',
            "La cantidad debe ser mayor que cero.",
        ),
        (
            "devuelta_no_negativa",
            'CHECK("iCantidadDevuelta" >= 0)',
            "La cantidad devuelta no puede ser negativa.",
        ),
        (
            "devuelta_no_supera",
            'CHECK("iCantidadDevuelta" <= "iCantidad")',
            "No se pueden devolver más unidades de las prestadas.",
        ),
    ]

    @api.depends("prestamo_id.sReferencia", "material_id.sNombre")
    def _compute_display_name(self):
        for record in self:
            record.display_name = "%s - %s" % (
                record.prestamo_id.sReferencia or "",
                record.material_id.sNombre or "",
            )

    @api.depends("iCantidad", "iCantidadDevuelta")
    def _compute_estado_devolucion(self):
        for record in self:
            if record.iCantidadDevuelta <= 0:
                record.selEstadoDevolucion = "pendiente"
            elif record.iCantidadDevuelta < record.iCantidad:
                record.selEstadoDevolucion = "parcial"
            else:
                record.selEstadoDevolucion = "completa"

    @api.onchange("iCantidadDevuelta", "iCantidad")
    def onchange_cantidad_devuelta(self):
        if self.iCantidadDevuelta > self.iCantidad:
            return {
                "value": {"iCantidadDevuelta": self.iCantidad},
                "warning": {
                    "title": "Cantidad devuelta excesiva",
                    "message": "No se pueden devolver más unidades de las prestadas; se ha ajustado al máximo.",
                },
            }
