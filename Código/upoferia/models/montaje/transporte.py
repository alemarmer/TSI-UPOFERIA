from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Transporte(models.Model):

    _name = "upoferia.transporte"
    _description = "Transporte"
    _rec_name = "numero"

    numero = fields.Char(
        string="Número", required=True, help="Identificador único del transporte"
    )
    fecha_prevista = fields.Datetime(string="Fecha prevista")
    fecha_realizada = fields.Datetime(string="Fecha realizada")
    estado = fields.Selection(
        [
            ("pendiente", "Pendiente"),
            ("en_ruta", "En ruta"),
            ("entregado", "Entregado"),
        ],
        "Estado",
        default="pendiente",
    )
    tipo_operacion = fields.Char(
        string="Tipo de operación", default="Transferencia interna"
    )
    ubicacion_origen = fields.Char(string="Ubicación de origen")
    ubicacion_destino = fields.Char(string="Ubicación de destino")

    # Relaciones
    tarea_montaje_id = fields.Many2one(
        "upoferia.tarea_montaje", string="Tarea de montaje", ondelete="set null"
    )

    _sql_constraints = [
        ("numero_unique", "UNIQUE(numero)", "Ya existe un transporte con ese número."),
    ]

    @api.constrains("numero")
    def _check_numero(self):
        for record in self:
            if not record.numero.strip():
                raise ValidationError("El número del transporte no puede estar vacío.")

    @api.onchange("estado")
    def onchange_estado(self):
        if self.estado == "entregado" and not self.fecha_realizada:
            self.fecha_realizada = fields.Datetime.now()
