# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MobiliarioCaseta(models.Model):
    _name = 'upoferia.mobiliario_caseta'
    _description = 'Mobiliario de caseta'
    _rec_name = 'sNumeroSerie'

    sNumeroSerie = fields.Char(string='Número de serie', required=True)
    sNombre = fields.Char(string='Nombre', required=True)
    dFechaAsignacion = fields.Date(string='Fecha de asignación')
    fCoste = fields.Float(string='Coste')

    caseta_id = fields.Many2one('upoferia.caseta', string='Caseta')

    _sql_constraints = [
            ('numero_serie_uniq', 'UNIQUE ("sNumeroSerie")',
             'Ya existe un mobiliario con ese número de serie.'),
    ]

    @api.constrains('fCoste')
    def _check_coste(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.fCoste < 0:
                raise models.ValidationError('El «Coste» del mobiliario no puede ser negativo.')
