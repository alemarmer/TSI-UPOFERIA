from odoo import models, fields


class TipoProducto(models.Model):

    _name = 'upoferia.tipo_producto'
    _description = 'Tipo de producto'
    _rec_name = 'nombre'

    nombre = fields.Char(string="Nombre", required=True, help="Identificador único del tipo de producto")