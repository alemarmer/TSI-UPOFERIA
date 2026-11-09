# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CategoriaProveedor(models.Model):
     _name = 'upoferia.categoria_proveedor'
     _description = 'Categoría de proveedor'
     _rec_name = 'sNombre'

     sNombre = fields.Char(string="Nombre", required=True)
     iColor = fields.Integer(string="Color", default=0)

     padre_id = fields.Many2one("upoferia.categoria_proveedor", string="Categoría padre")
     hija_ids = fields.One2many("upoferia.categoria_proveedor", 'padre_id', string="Subcategorías")
     proveedor_ids = fields.Many2many("upoferia.proveedor", 'upoferia_proveedor_categoria_rel', 'categoria_proveedor_id', 'proveedor_id', string="Proveedores")

     _sql_constraints = [('categoria_proveedor_nombre_unique', 'UNIQUE ("sNombre")', 'Ya existe una categoría de proveedor con ese nombre')]

     @api.constrains('padre_id')
     def _check_padre(self):
          for record in self:
               padre = record.padre_id
               while padre:
                    if padre == record:
                         raise models.ValidationError('Una categoría no puede ser su propia madre ni tener como madre a una de sus subcategorías.')
                    padre = padre.padre_id

     @api.constrains('sNombre')
     def _check_nombre(self):
          for record in self:
               if len(record.sNombre.strip()) < 2 or len(record.sNombre.strip()) > 50:
                    raise models.ValidationError('El nombre debe tener entre 2 y 50 caracteres.')

     @api.constrains('iColor')
     def _check_color(self):
          for record in self:
               if record.iColor < 0 or record.iColor > 11:
                    raise models.ValidationError('El color debe ser un número entre 0 y 11.')