# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ZonaCaseta(models.Model):
    _name = 'feria.zona_caseta'
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

    caseta_id = fields.Many2one('feria.caseta', string='Caseta', required=True, ondelete='cascade')
    mesa_ids = fields.One2many('feria.mesa', 'zona_id', string='Mesas')

    @api.depends('sNombre', 'caseta_id.sNombre')
    def _compute_display_name(self):
        oRegistro = None
        for oRegistro in self:
            oRegistro.display_name = f'{oRegistro.caseta_id.sNombre or ""} / {oRegistro.sNombre or ""}'

    @api.constrains('sNombre')
    def _check_nombre(self):
        oRegistro = None
        sNombre = ''
        for oRegistro in self:
            sNombre = oRegistro.sNombre or ''
            if not sNombre.strip():
                raise ValidationError('El campo «Nombre» es obligatorio.')
            if sNombre != sNombre.strip():
                raise ValidationError('El nombre de la zona no puede empezar ni terminar con espacios.')
            if not 2 <= len(sNombre) <= 50:
                raise ValidationError('El nombre de la zona debe tener entre 2 y 50 caracteres.')

    @api.constrains('fSuperficieM2')
    def _check_superficie_m2(self):
        oRegistro = None
        fSuperficie = 0.0
        for oRegistro in self:
            fSuperficie = oRegistro.fSuperficieM2
            if fSuperficie < 0:
                raise ValidationError('La «Superficie» de la zona no puede ser negativa.')
            if fSuperficie > 5000:
                raise ValidationError('La «Superficie» de la zona puede ser como mucho de 5.000 m².')
            if round(fSuperficie, 2) != fSuperficie:
                raise ValidationError('La «Superficie» de la zona solo admite dos decimales.')
