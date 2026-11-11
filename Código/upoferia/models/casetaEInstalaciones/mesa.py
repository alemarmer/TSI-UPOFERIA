# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Mesa(models.Model):
    _name = 'upoferia.mesa'
    _description = 'Mesa'
    _rec_name = 'iNumero'
    _sql_constraints = [
        ('numero_uniq', 'UNIQUE ("iNumero")',
         'Ya existe una mesa con ese número.'),
    ]

    iNumero = fields.Integer(string='Número', required=True)
    iCapacidad = fields.Integer(string='Capacidad', required=True)

    zona_id = fields.Many2one('upoferia.zona_caseta', string='Zona')

    @api.depends('iNumero', 'zona_id.display_name')
    def _compute_display_name(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.zona_id:
                oRegistro.display_name = f'Mesa {oRegistro.iNumero} ({oRegistro.zona_id.display_name})'
            else:
                oRegistro.display_name = f'Mesa {oRegistro.iNumero}'

    @api.constrains('iNumero')
    def _check_numero(self):
        oRegistro = None
        for oRegistro in self:
            if not 1 <= oRegistro.iNumero <= 9999:
                raise models.ValidationError('El «Número» de la mesa debe estar entre 1 y 9999.')

    @api.constrains('iCapacidad')
    def _check_capacidad(self):
        oRegistro = None
        for oRegistro in self:
            if not 1 <= oRegistro.iCapacidad <= 50:
                raise models.ValidationError('La «Capacidad» de la mesa debe estar entre 1 y 50 personas.')
