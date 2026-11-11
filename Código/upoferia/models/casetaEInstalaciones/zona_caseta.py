# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ZonaCaseta(models.Model):
    _name = 'upoferia.zona_caseta'
    _description = 'Zona de caseta'
    _rec_name = 'sNombre'
    _rec_names_search = ['sNombre', 'caseta_id.sNombre']
    _sql_constraints = [
        ('caseta_nombre_uniq', 'UNIQUE (caseta_id, "sNombre")',
         'Esa caseta ya tiene una zona con ese nombre.'),
    ]

    sNombre = fields.Char(string='Nombre', required=True)
    sTipo = fields.Selection([
        ('comedor', 'Comedor'),
        ('barra', 'Barra'),
        ('cocina', 'Cocina'),
        ('baile', 'Zona de baile'),
        ('escenario', 'Escenario'),
        ('reservado', 'Reservado'),
        ('almacen', 'Almacén'),
        ('aseos', 'Aseos'),
    ], string='Tipo')
    fSuperficieM2 = fields.Float(string='Superficie (m²)')

    caseta_id = fields.Many2one('upoferia.caseta', string='Caseta', required=True)
    mesa_ids = fields.One2many('upoferia.mesa', 'zona_id', string='Mesas')

    @api.depends('sNombre', 'caseta_id.sNombre')
    def _compute_display_name(self):
        oRegistro = None
        for oRegistro in self:
            oRegistro.display_name = f'{oRegistro.caseta_id.sNombre or ""} / {oRegistro.sNombre or ""}'

    @api.constrains('fSuperficieM2')
    def _check_superficie_m2(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.fSuperficieM2 < 0:
                raise models.ValidationError('La «Superficie» de la zona no puede ser negativa.')
