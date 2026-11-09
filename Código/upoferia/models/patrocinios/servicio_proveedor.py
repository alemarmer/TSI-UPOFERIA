# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ServicioProveedor(models.Model):
     _name = 'upoferia.servicio_proveedor'
     _description = 'Servicio ofrecido por un proveedor'
     _rec_name = 'servicio_id'

     fPrecioTarifa = fields.Float(string="Precio de tarifa", required=True)

     
     servicio_id = fields.Many2one("upoferia.servicio", string="Servicio", required=True)
     proveedor_id = fields.Many2one("upoferia.proveedor", string="Proveedor", required=True)

     _sql_constraints = [('servicio_proveedor_unique', 'UNIQUE ("servicio_id", "proveedor_id")', 'Este proveedor ya tiene una tarifa para ese servicio')]

     @api.constrains('fPrecioTarifa')
     def _check_precio_tarifa(self):
          for record in self:
               if record.fPrecioTarifa < 0:
                    raise models.ValidationError('El precio de tarifa no puede ser menor que 0.')
