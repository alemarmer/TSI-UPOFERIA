# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Llave(models.Model):
    _name = 'upoferia.llave'
    _description = 'Llave'
    _rec_name = 'sCodigoLlave'
    _sql_constraints = [
        ('codigo_llave_uniq', 'UNIQUE ("sCodigoLlave")',
         'Ya existe una llave con ese código.'),
    ]

    sCodigoLlave = fields.Char(string='Código de llave', required=True)
    sDescripcion = fields.Char(string='Descripción')
    sTipo = fields.Selection([
        ('maestra', 'Maestra'),
        ('original', 'Original'),
    ], string='Tipo', required=True, default='original')

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
