# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Proveedor(models.Model):
     _name = 'upoferia.proveedor'
     _description = 'Proveedor'
     _inherits = {'upoferia.persona': 'persona_id'}
     _rec_name = 'sNombre'

     persona_id = fields.Many2one("upoferia.persona", string="Persona", required=True, ondelete='cascade')

     sCif = fields.Char(string="CIF", size=9)

     
     transaccion_ids = fields.One2many("upoferia.transaccion", 'proveedor_id', string="Transacciones")
     categoria_ids = fields.Many2many("upoferia.categoria_proveedor", 'upoferia_proveedor_categoria_rel', 'proveedor_id', 'categoria_proveedor_id', string="Categorías")
     marca_ids = fields.One2many("upoferia.marca", 'proveedor_id', string="Marcas")
     servicio_proveedor_ids = fields.One2many("upoferia.servicio_proveedor", 'proveedor_id', string="Servicios que ofrece")
     prestamo_ids = fields.One2many("upoferia.prestamo", 'proveedor_id', string="Préstamos")

     _sql_constraints = [('proveedor_cif_unique', 'UNIQUE ("sCif")', 'Ya existe un proveedor con ese CIF')]

     def btn_eliminarTarifas(self):
          for tarifa in self.servicio_proveedor_ids:
               self.write({'servicio_proveedor_ids':[(2,tarifa.id)]})
               
     @api.constrains('sCif')
     def _check_cif(self):
          for record in self:
               if record.sCif and len(record.sCif) != 9:
                    raise models.ValidationError('El CIF debe tener 9 caracteres (por ejemplo B12345674).')
