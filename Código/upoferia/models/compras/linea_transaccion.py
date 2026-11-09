# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LineaTransaccion(models.Model):
     _name = 'upoferia.linea_transaccion'
     _description = 'Línea de transacción'
     _rec_name = 'iNumeroLinea'
     _rec_names_search = ['transaccion_id', 'iNumeroLinea']

     iNumeroLinea = fields.Integer(string="Número de línea", required=True)
     iCantidad = fields.Integer(string="Cantidad", required=True)
     iCantidadRecibida = fields.Integer(string="Cantidad recibida")
     fPrecioUnitario = fields.Float(string="Precio unitario")

     
     transaccion_id = fields.Many2one("upoferia.transaccion", string="Transacción", required=True)
     linea_pedido_id = fields.Many2one("upoferia.linea_transaccion", string="Línea de pedido")
     linea_factura_ids = fields.One2many("upoferia.linea_transaccion", 'linea_pedido_id', string="Líneas de factura")
     producto_id = fields.Many2one("upoferia.producto", string="Producto")
     fSubtotal = fields.Float(compute='_subtotal', string="Subtotal")
     iCantidadFacturada = fields.Integer(compute='_cantidadFacturada', string="Cantidad facturada")

     _sql_constraints = [('linea_transaccion_numero_unique', 'UNIQUE ("transaccion_id", "iNumeroLinea")', 'Ya existe una línea con ese número en esta transacción')]

     @api.depends('transaccion_id.sIdTransaccion', 'iNumeroLinea')
     def _compute_display_name(self):
          for record in self:
               record.display_name = '%s / %s' % (record.transaccion_id.sIdTransaccion or '', record.iNumeroLinea)

     @api.depends('iCantidad', 'fPrecioUnitario')
     def _subtotal(self):
          for record in self:
               record.fSubtotal = record.iCantidad * record.fPrecioUnitario

     @api.depends('linea_factura_ids.iCantidad')
     def _cantidadFacturada(self):
          for record in self:
               record.iCantidadFacturada = sum(record.linea_factura_ids.mapped('iCantidad'))

     @api.constrains('iCantidad', 'iCantidadRecibida')
     def _check_cantidades(self):
          for record in self:
               if record.iCantidad <= 0:
                    raise models.ValidationError('La cantidad debe ser mayor que 0.')
               if record.iCantidadRecibida < 0 or record.iCantidadRecibida > record.iCantidad:
                    raise models.ValidationError('La cantidad recibida debe estar entre 0 y la cantidad de la línea.')

     @api.constrains('fPrecioUnitario')
     def _check_precio_unitario(self):
          for record in self:
               if record.fPrecioUnitario < 0:
                    raise models.ValidationError('El precio unitario no puede ser menor que 0.')
