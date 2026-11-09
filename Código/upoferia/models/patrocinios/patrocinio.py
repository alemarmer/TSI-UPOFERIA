# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Patrocinio(models.Model):
     _name = 'upoferia.patrocinio'
     _description = 'Patrocinio de una marca a un evento'

     fImporteAportacion = fields.Float(string="Importe de la aportación")
     sTipoAportacion = fields.Selection([('economica', 'Económica'),
                                         ('especie', 'En especie'),],
                                         'Tipo de aportación')

     
     marca_id = fields.Many2one("upoferia.marca", string="Marca", required=True, ondelete='cascade')
     evento_id = fields.Many2one("upoferia.evento", string="Evento", required=True, ondelete='cascade')

     _sql_constraints = [('patrocinio_marca_evento_unique', 'UNIQUE ("marca_id", "evento_id")', 'Esa marca ya patrocina ese evento')]

     @api.depends('marca_id.sNombre', 'evento_id')
     def _compute_display_name(self):
          for record in self:
               record.display_name = '%s → %s' % (record.marca_id.sNombre or '', record.evento_id.display_name or '')

     @api.constrains('fImporteAportacion')
     def _check_importe_aportacion(self):
          for record in self:
               if record.fImporteAportacion < 0:
                    raise models.ValidationError('El importe de la aportación no puede ser menor que 0.')
