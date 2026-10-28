from odoo import models, fields


class LineaTicket(models.Model):

    _name = 'upoferia.linea_ticket'
    _description = 'Línea de ticket'

    numero_linea = fields.Integer(string="Nº de línea", required=True, help="Identifica la línea dentro de su ticket")
    cantidad = fields.Integer(string="Cantidad", required=True, default=1)
    precio_unitario = fields.Float(string="Precio unitario", required=True, digits=(10, 2))