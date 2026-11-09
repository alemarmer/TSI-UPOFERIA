# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CategoriaProveedor(models.Model):
     _name = 'upoferia.categoria_proveedor'
     _description = 'Categoría de proveedor'
     _rec_name = 'sNombre'

     sNombre = fields.Char(string="Nombre", required=True)
     iColor = fields.Integer(string="Color", default=0)
     padre_id = fields.Many2one("upoferia.categoria_proveedor", string="Categoría padre", ondelete='restrict')
     hija_ids = fields.One2many("upoferia.categoria_proveedor", 'padre_id', string="Subcategorías")
     proveedor_ids = fields.Many2many("upoferia.proveedor", 'upoferia_proveedor_categoria_rel', 'categoria_proveedor_id', 'proveedor_id', string="Proveedores")

     _sql_constraints = [('categoria_proveedor_nombre_unique', 'UNIQUE ("sNombre")', 'Ya existe una categoría de proveedor con ese nombre')]

     @api.constrains('padre_id')
     def _check_padre(self):
          if self._has_cycle('padre_id'):
               raise models.ValidationError('Una categoría no puede ser su propia madre ni tener como madre a una de sus subcategorías.')
