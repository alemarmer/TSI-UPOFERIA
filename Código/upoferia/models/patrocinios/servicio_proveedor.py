from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ServicioProveedor(models.Model):
    _name = 'feria.servicio_proveedor'
    _description = 'Servicio ofrecido por un proveedor'
    _rec_name = 'servicio_id'
    _sql_constraints = [
        ('servicio_proveedor_uniq', 'UNIQUE ("servicio_id", "proveedor_id")',
         'Este proveedor ya tiene una tarifa para ese servicio.'),
    ]

    fPrecioTarifa = fields.Float(string='Precio de tarifa')

    servicio_id = fields.Many2one('feria.servicio', string='Servicio', required=True, ondelete='cascade')
    proveedor_id = fields.Many2one('feria.proveedor', string='Proveedor', required=True, ondelete='cascade')
