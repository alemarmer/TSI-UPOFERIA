# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Actuacion(models.Model):
    _name = 'upoferia.actuacion'
    _description = 'Actuación'
    _rec_name = 'sNombre_evento'
    _inherits = {'upoferia.evento': 'evento_id'}

    fCache_pactado = fields.Float(string='Caché pactado')

    evento_id = fields.Many2one('upoferia.evento', string='Evento', required=True)
    transaccion_id = fields.Many2one('upoferia.transaccion', string='Contrato')
    servicio_ids = fields.Many2many('upoferia.servicio', 'upoferia_actuacion_servicio', 'actuacion_id', 'servicio_id', string='Servicios')
    artista_ids = fields.Many2many('upoferia.artista', 'upoferia_actuacion_artista',
                                   'actuacion_id', 'artista_id', string='Artistas')
    iNum_artistas = fields.Integer(compute='_numArtistas', string='Número de artistas', store=True)

    _sql_constraints = [('actuacion_evento_unique', 'UNIQUE ("evento_id")', 'Ese evento ya está registrado como actuación.')]

    def btn_quitarArtistas(self):
        for artista in self.artista_ids:
            self.write({'artista_ids': [(3, artista.id)]})

    @api.depends('artista_ids')
    def _numArtistas(self):
        for record in self:
            record.iNum_artistas = len(record.artista_ids)

    @api.constrains('fCache_pactado')
    def _check_fCache_pactado(self):
        for record in self:
            if record.fCache_pactado < 0:
                raise models.ValidationError('El caché pactado no puede ser negativo.')

    @api.constrains('transaccion_id')
    def _check_transaccion(self):
        for record in self:
            if record.transaccion_id and record.transaccion_id.tipo_transaccion_id.sCodigo != 'CON':
                raise models.ValidationError('Una actuación solo se puede asociar a un contrato (CON).')

    @api.onchange('artista_ids')
    def onchange_artista_ids(self):
        resultado = {
            'value': {'fCache_pactado': sum(self.artista_ids.mapped('fCache_base'))}
        }
        return resultado
