# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Llave(models.Model):
    _name = 'upoferia.llave'
    _description = 'Llave'
    _rec_name = 'sCodigoLlave'

    sCodigoLlave = fields.Char(string='Código de llave', required=True)
    sDescripcion = fields.Char(string='Descripción')
    sTipo = fields.Selection([
        ('maestra', 'Maestra'),
        ('original', 'Original'),
    ], string='Tipo', required=True, default='original')

    numero = fields.Many2one('upoferia.taquilla', string='Taquilla')

    _sql_constraints = [
            ('codigo_llave_uniq', 'UNIQUE ("sCodigoLlave")',
             'Ya existe una llave con ese código.'),
            ('taquilla_uniq', 'UNIQUE (taquilla_id)',
             'Esa taquilla ya tiene una llave.'),
    ]

    @api.constrains('sTipo')
    def _check_tipo(self):
        oRegistro = None
        iMaestras = 0
        for oRegistro in self:
            if oRegistro.sTipo != 'maestra':
                continue
            iMaestras = self.search_count([('sTipo', '=', 'maestra'), ('id', '!=', oRegistro.id)])
            if iMaestras > 0:
                raise models.ValidationError('Ya existe una llave maestra: solo puede haber una.')
