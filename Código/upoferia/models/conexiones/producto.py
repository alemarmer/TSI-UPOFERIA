from odoo import models, fields


class Producto(models.Model):
    _inherit = 'upoferia.producto'

    marca_id = fields.Many2one('feria.marca', string='Marca', ondelete='set null')
    linea_transaccion_ids = fields.One2many('feria.linea_transaccion', 'producto_id', string='Líneas de transacción')
