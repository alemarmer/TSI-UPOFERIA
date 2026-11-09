# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EspacioPublicitario(models.Model):
     _name = 'upoferia.espacio_publicitario'
     _description = 'Espacio publicitario'
     _rec_name = 'sCodigoLugar'

     sCodigoLugar = fields.Char(string="Código del lugar", required=True)
     sTipo = fields.Selection([('lona', 'Lona'),
                               ('valla', 'Valla'),
                               ('banderola', 'Banderola'),
                               ('pantalla', 'Pantalla digital'),
                               ('photocall', 'Photocall'),
                               ('mupi', 'Mupi'),
                               ('suelo', 'Vinilo de suelo'),],
                               'Tipo')
     sUbicacionExacta = fields.Char(string="Ubicación exacta")
     fAltoM = fields.Float(string="Alto (m)", required=True)
     fAnchoM = fields.Float(string="Ancho (m)", required=True)
     bIluminado = fields.Boolean(string="Iluminado")

     
     exhibicion_ids = fields.One2many("upoferia.exhibicion_marca", 'espacio_publicitario_id', string="Exhibiciones")
     zona_caseta_id = fields.Many2one("upoferia.zona_caseta", string="Zona de la caseta")
     fSuperficieM2 = fields.Float(compute='_superficie', string="Superficie (m²)")

     _sql_constraints = [('espacio_publicitario_codigo_unique', 'UNIQUE ("sCodigoLugar")', 'Ya existe un espacio publicitario con ese código')]

     @api.depends('fAltoM', 'fAnchoM')
     def _superficie(self):
          for record in self:
               record.fSuperficieM2 = record.fAltoM * record.fAnchoM

     @api.constrains('fAltoM', 'fAnchoM')
     def _check_medidas(self):
          for record in self:
               if record.fAltoM <= 0 or record.fAnchoM <= 0:
                    raise models.ValidationError('El alto y el ancho deben ser mayores que 0.')
               if record.fAltoM > 30 or record.fAnchoM > 30:
                    raise models.ValidationError('El alto y el ancho no pueden superar los 30 metros.')

     @api.onchange('fAltoM', 'fAnchoM')
     def onchange_medidas(self):
          resultado = {}
          if self.fAltoM > 30 or self.fAnchoM > 30:
               resultado = {
                    'value': {'fAltoM': min(self.fAltoM, 30), 'fAnchoM': min(self.fAnchoM, 30)},
                    'warning': {
                         'title': 'Valores incorrectos',
                         'message': 'El alto y el ancho no pueden superar los 30 metros; se han ajustado a 30.'
                    }
               }
               return resultado
