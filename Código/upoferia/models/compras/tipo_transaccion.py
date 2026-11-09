# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TipoTransaccion(models.Model):
     _name = 'upoferia.tipo_transaccion'
     _description = 'Tipo de transacción'
     _rec_name = 'sCodigo'

     sCodigo = fields.Char(string="Código", required=True)
     sNombre = fields.Char(string="Nombre", required=True)
     sDescripcion = fields.Char(string="Descripción")
     
     transaccion_ids = fields.One2many("upoferia.transaccion", 'tipo_transaccion_id', string="Transacciones")

     _sql_constraints = [('tipo_transaccion_codigo_unique', 'UNIQUE ("sCodigo")', 'Ya existe un tipo de transacción con ese código')]

     @api.constrains('sCodigo')
     def _check_codigo(self):
          for record in self:
               if record.sCodigo not in ('PED', 'ALB', 'FAC', 'ABO', 'CON'):
                    raise models.ValidationError('El código debe ser PED, ALB, FAC, ABO o CON.')
