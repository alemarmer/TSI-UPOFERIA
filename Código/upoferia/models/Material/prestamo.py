from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class Prestamo(models.Model):

    _name = "upoferia.prestamo"
    _description = "Préstamo de material"
    _rec_name = "referencia"
    _order = "fecha_inicio desc, id desc"

    referencia = fields.Char(
        string="Referencia", required=True, help="Identificador único del préstamo"
    )
    fecha_inicio = fields.Date(string="Fecha de inicio", required=True)
    fecha_fin_prevista = fields.Date(string="Fecha fin prevista")
    fecha_devolucion = fields.Date(string="Fecha de devolución")
    importe = fields.Float(string="Importe", digits=(10, 2))
    estado = fields.Selection(
        [
            ("solicitado", "Solicitado"),
            ("en_curso", "En curso"),
            ("devuelto", "Devuelto"),
        ],
        "Estado",
        default="solicitado",
    )
    responsable = fields.Char(string="Responsable")

    # Relaciones
    proveedor_id = fields.Many2one(
        "upoferia.proveedor", string="Proveedor", ondelete="set null"
    )
    transaccion_id = fields.Many2one(
        "upoferia.transaccion", string="Transacción (contrato)", ondelete="set null"
    )
    prestamo_linea_ids = fields.One2many(
        "upoferia.prestamo_linea", "prestamo_id", string="Líneas"
    )

    _sql_constraints = [
        (
            "referencia_unique",
            "UNIQUE(referencia)",
            "Ya existe un préstamo con esa referencia.",
        ),
        (
            "importe_no_negativo",
            "CHECK(importe >= 0)",
            "El importe no puede ser negativo.",
        ),
        (
            "fin_prevista_orden",
            "CHECK(fecha_fin_prevista >= fecha_inicio)",
            "La fecha fin prevista no puede ser anterior a la de inicio.",
        ),
        (
            "devolucion_orden",
            "CHECK(fecha_devolucion >= fecha_inicio)",
            "La fecha de devolución no puede ser anterior a la de inicio.",
        ),
    ]

    @api.constrains("referencia")
    def _check_referencia(self):
        for record in self:
            if not record.referencia.strip():
                raise ValidationError(
                    "La referencia del préstamo no puede estar vacía."
                )

    @api.onchange("fecha_inicio")
    def onchange_fecha_inicio(self):
        if self.fecha_inicio and not self.fecha_fin_prevista:
            self.fecha_fin_prevista = self.fecha_inicio + timedelta(days=14)

    @api.onchange("fecha_devolucion")
    def onchange_fecha_devolucion(self):
        if self.fecha_devolucion:
            self.estado = "devuelto"
