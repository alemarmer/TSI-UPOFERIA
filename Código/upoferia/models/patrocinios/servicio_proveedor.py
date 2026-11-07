from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ServicioProveedor(models.Model):
    _name = 'upoferia.servicio_proveedor'
    _description = 'Servicio ofrecido por un proveedor'
    _rec_name = 'servicio_id'
    _sql_constraints = [
        ('servicio_proveedor_uniq', 'UNIQUE ("servicio_id", "proveedor_id")',
         'Este proveedor ya tiene una tarifa para ese servicio.'),
    ]

    fPrecioTarifa = fields.Float(string='Precio de tarifa', required=True)

    servicio_id = fields.Many2one('upoferia.servicio', string='Servicio', required=True, ondelete='cascade')
    proveedor_id = fields.Many2one('upoferia.proveedor', string='Proveedor', required=True, ondelete='cascade')

    @api.constrains('fPrecioTarifa')
    def _check_precio_tarifa(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.fPrecioTarifa < 0:
                raise ValidationError('«Precio de tarifa» no puede ser menor que 0.')
            if oRegistro.fPrecioTarifa > 1000000:
                raise ValidationError('«Precio de tarifa» no puede superar 1.000.000 €.')
            if round(oRegistro.fPrecioTarifa, 2) != oRegistro.fPrecioTarifa:
                raise ValidationError('«Precio de tarifa» solo admite dos decimales (céntimos).')
