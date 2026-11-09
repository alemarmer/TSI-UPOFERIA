# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ExhibicionMarca(models.Model):
     _name = 'upoferia.exhibicion_marca'
     _description = 'Exhibición de marca'
     _rec_name = 'sIdExhibicion'

     sIdExhibicion = fields.Char(string="Id. exhibición", required=True)
     dFechaMontaje = fields.Date(string="Fecha de montaje")
     dFechaRetirada = fields.Date(string="Fecha de retirada")
     sArteFinal = fields.Char(string="Arte final")

     
     marca_id = fields.Many2one("upoferia.marca", string="Marca", required=True, ondelete='restrict')
     espacio_publicitario_id = fields.Many2one("upoferia.espacio_publicitario", string="Espacio publicitario", required=True, ondelete='restrict')
     tecnico_id = fields.Many2one("upoferia.tecnico", string="Técnico", ondelete='set null')
     sEstadoExhibicion = fields.Selection([('sin_programar', 'Sin programar'),
                                           ('programada', 'Programada'),
                                           ('montada', 'Montada'),
                                           ('retirada', 'Retirada'),],
                                           'Estado', compute='_estadoExhibicion')

     _sql_constraints = [('exhibicion_marca_id_unique', 'UNIQUE ("sIdExhibicion")', 'Ya existe una exhibición con ese identificador')]

     @api.depends('dFechaMontaje', 'dFechaRetirada')
     def _estadoExhibicion(self):
          hoy = fields.Date.context_today(self)
          for record in self:
               if not record.dFechaMontaje:
                    record.sEstadoExhibicion = 'sin_programar'
               elif hoy < record.dFechaMontaje:
                    record.sEstadoExhibicion = 'programada'
               elif not record.dFechaRetirada or hoy <= record.dFechaRetirada:
                    record.sEstadoExhibicion = 'montada'
               else:
                    record.sEstadoExhibicion = 'retirada'

     @api.constrains('dFechaMontaje', 'dFechaRetirada')
     def _check_fechas(self):
          for record in self:
               if record.dFechaRetirada and not record.dFechaMontaje:
                    raise models.ValidationError('No se puede indicar la fecha de retirada sin la fecha de montaje.')
               if record.dFechaRetirada and record.dFechaRetirada < record.dFechaMontaje:
                    raise models.ValidationError('La fecha de retirada no puede ser anterior a la fecha de montaje.')

     @api.constrains('dFechaMontaje', 'dFechaRetirada', 'espacio_publicitario_id')
     def _check_solapamiento(self):
          for record in self:
               if not record.dFechaMontaje:
                    continue
               otras = self.search([('espacio_publicitario_id', '=', record.espacio_publicitario_id.id), ('id', '!=', record.id)])
               for otra in otras:
                    if not otra.dFechaMontaje:
                         continue
                    # Sin fecha de retirada, la exhibición ocupa el espacio desde el montaje en adelante
                    empieza_antes = not record.dFechaRetirada or otra.dFechaMontaje <= record.dFechaRetirada
                    acaba_despues = not otra.dFechaRetirada or otra.dFechaRetirada >= record.dFechaMontaje
                    if empieza_antes and acaba_despues:
                         raise models.ValidationError('El espacio %s ya está ocupado en esas fechas por la exhibición %s.' % (record.espacio_publicitario_id.sCodigoLugar, otra.sIdExhibicion))
