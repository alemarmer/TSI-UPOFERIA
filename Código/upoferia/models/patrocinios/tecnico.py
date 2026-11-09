# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Tecnico(models.Model):
     _name = 'upoferia.tecnico'
     _description = 'Técnico'
     _inherits = {'upoferia.persona': 'persona_id'}
     _rec_name = 'sNombre'

     persona_id = fields.Many2one("upoferia.persona", string="Persona", required=True, ondelete='cascade')

     sEspecialidad = fields.Selection([('electricidad', 'Electricidad'),
                                       ('sonido', 'Sonido'),
                                       ('iluminacion', 'Iluminación'),
                                       ('montaje', 'Montaje y estructuras'),
                                       ('fontaneria', 'Fontanería'),
                                       ('climatizacion', 'Climatización'),
                                       ('gas', 'Gas'),],
                                       'Especialidad')
     sCodCarnetProfesional = fields.Char(string="Código del carné profesional")
     dFechaCaducidadCarnet = fields.Date(string="Caducidad del carné")

     
     exhibicion_ids = fields.One2many("upoferia.exhibicion_marca", 'tecnico_id', string="Exhibiciones")
     mantenimiento_ids = fields.Many2many("upoferia.mantenimiento", 'upoferia_mantenimiento_tecnico', 'tecnico_id', 'mantenimiento_id', string="Mantenimientos")

     _sql_constraints = [('tecnico_carnet_unique', 'UNIQUE ("sCodCarnetProfesional")', 'Ya existe un técnico con ese código de carné profesional')]

     def btn_quitarExhibiciones(self):
          self.write({'exhibicion_ids':[(5,)]})     

     @api.onchange('dFechaCaducidadCarnet')
     def onchange_caducidad_carnet(self):
          resultado = {}
          if self.dFechaCaducidadCarnet and self.dFechaCaducidadCarnet < fields.Date.context_today(self):
               resultado = {
                    'warning': {
                         'title': 'Carné caducado',
                         'message': 'El carné profesional de este técnico ya está caducado.'
                    }
               }
               return resultado

     @api.constrains('sCodCarnetProfesional', 'dFechaCaducidadCarnet')
     def _check_carnet(self):
          for record in self:
               if record.dFechaCaducidadCarnet and not record.sCodCarnetProfesional:
                    raise models.ValidationError('No se puede indicar la caducidad del carné sin el código del carné.')