from odoo import models, fields


class TipoCuota(models.Model):

    _name = 'upoferia.tipo_cuota'
    _description = 'Tipo de cuota'
    _rec_name = 'nombre'

    nombre = fields.Char(string="Nombre", required=True, help="Identificador único del tipo de cuota")
    importe = fields.Float(string="Importe", required=True, digits=(10, 2))