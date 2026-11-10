from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class Prestamo(models.Model):

    _name = "upoferia.prestamo"
    _description = "Préstamo de material"
    _rec_name = "sReferencia"
    _order = "dFechaInicio desc, id desc"

    sReferencia = fields.Char(
        string="Referencia", required=True, help="Identificador único del préstamo"
    )
    dFechaInicio = fields.Date(string="Fecha de inicio", required=True)
    dFechaFinPrevista = fields.Date(string="Fecha fin prevista")
    dFechaDevolucion = fields.Date(string="Fecha de devolución")
    fImporte = fields.Float(string="Importe", digits=(10, 2))
    selEstado = fields.Selection(
        [
            ("solicitado", "Solicitado"),
            ("en_curso", "En curso"),
            ("devuelto", "Devuelto"),
        ],
        "Estado",
        default="solicitado",
    )
    sResponsable = fields.Char(string="Responsable")

    # Relaciones
    # PENDIENTE DE INTEGRAR CON COMPRAS (necesitan upoferia.proveedor y upoferia.transaccion):
    # proveedor_id = fields.Many2one('upoferia.proveedor', string="Proveedor")
    # transaccion_id = fields.Many2one('upoferia.transaccion', string="Transacción (contrato)")
    prestamo_linea_ids = fields.One2many(
        "upoferia.prestamo_linea", "prestamo_id", string="Líneas"
    )

    _sql_constraints = [
        (
            "referencia_unique",
            'UNIQUE("sReferencia")',
            "Ya existe un préstamo con esa referencia.",
        ),
    ]

    @api.constrains("sReferencia")
    def _check_referencia(self):
        for record in self:
            if not record.sReferencia.strip():
                raise ValidationError(
                    "La referencia del préstamo no puede estar vacía."
                )

    @api.constrains("fImporte", "dFechaInicio", "dFechaFinPrevista", "dFechaDevolucion")
    def _check_importe_fechas(self):
        for record in self:
            if record.fImporte < 0:
                raise ValidationError("El importe no puede ser negativo.")
            if record.dFechaFinPrevista and record.dFechaFinPrevista < record.dFechaInicio:
                raise ValidationError(
                    "La fecha fin prevista no puede ser anterior a la de inicio."
                )
            if record.dFechaDevolucion and record.dFechaDevolucion < record.dFechaInicio:
                raise ValidationError(
                    "La fecha de devolución no puede ser anterior a la de inicio."
                )

    @api.onchange("dFechaInicio")
    def onchange_fecha_inicio(self):
        if self.dFechaInicio and not self.dFechaFinPrevista:
            self.dFechaFinPrevista = self.dFechaInicio + timedelta(days=14)

    @api.onchange("dFechaDevolucion")
    def onchange_fecha_devolucion(self):
        if self.dFechaDevolucion:
            self.selEstado = "devuelto"
