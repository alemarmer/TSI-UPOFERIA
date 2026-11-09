# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Tecnico(models.Model):
     _name = 'upoferia.tecnico'
     _description = 'Técnico'

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

     _sql_constraints = [('tecnico_carnet_unique', 'UNIQUE ("sCodCarnetProfesional")', 'Ya existe un técnico con ese código de carné profesional')]

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
