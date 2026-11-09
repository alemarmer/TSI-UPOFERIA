# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Marca(models.Model):
     _name = 'upoferia.marca'
     _description = 'Marca'
     _rec_name = 'sNombre'

     sNombre = fields.Char(string="Nombre", required=True)
     binLogotipo = fields.Image(string="Logotipo", max_width=512, max_height=512)
     sColorCorporativo = fields.Char(string="Color corporativo")

     
     proveedor_id = fields.Many2one("upoferia.proveedor", string="Proveedor")
     exhibicion_ids = fields.One2many("upoferia.exhibicion_marca", 'marca_id', string="Exhibiciones")
     patrocinio_ids = fields.One2many("upoferia.patrocinio", 'marca_id', string="Patrocinios")
     producto_ids = fields.One2many("upoferia.producto", 'marca_id', string="Productos")

     _sql_constraints = [('marca_nombre_unique', 'UNIQUE ("sNombre")', 'Ya existe una marca con ese nombre')]


     def btn_eliminarPatrocinios(self):
          for patrocinio in self.patrocinio_ids:
               self.write({'patrocinio_ids':[(2,patrocinio.id)]})

     @api.constrains('sNombre')
     def _check_nombre(self):
          for record in self:
               if len(record.sNombre.strip()) < 2 or len(record.sNombre.strip()) > 50:
                    raise models.ValidationError('El nombre debe tener entre 2 y 50 caracteres.')