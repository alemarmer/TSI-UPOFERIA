from odoo import models, fields


class Ticket(models.Model):

    _name = 'upoferia.ticket'
    _description = 'Ticket de consumición'
    _rec_name = 'referencia'

    referencia = fields.Char(string="Referencia", required=True, help="Identificador único del ticket")
    fecha = fields.Datetime(string="Fecha", required=True, default=fields.Datetime.now)