# -*- coding: utf-8 -*-

import re

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

    @api.constrains('sCodigoLlave')
    def _check_codigo_llave(self):
        oRegistro = None
        sCodigoLlave = ''
        for oRegistro in self:
            sCodigoLlave = oRegistro.sCodigoLlave or ''
            if not sCodigoLlave.strip():
                raise models.ValidationError('El campo «Código de llave» es obligatorio.')
            if not 2 <= len(sCodigoLlave) <= 20:
                raise models.ValidationError('El «Código de llave» debe tener entre 2 y 20 caracteres.')
            if not re.fullmatch(r'[A-Z0-9]+([-/._][A-Z0-9]+)*', sCodigoLlave):
                raise models.ValidationError('El «Código de llave» solo puede tener letras mayúsculas y números, separados por - / . _ y sin espacios (por ejemplo LL-T-014).')

    @api.constrains('sDescripcion')
    def _check_descripcion(self):
        oRegistro = None
        sDescripcion = ''
        for oRegistro in self:
            sDescripcion = oRegistro.sDescripcion or ''
            if not sDescripcion:
                continue
            if sDescripcion != sDescripcion.strip():
                raise models.ValidationError('La «Descripción» de la llave no puede empezar ni terminar con espacios.')
            if len(sDescripcion) > 255:
                raise models.ValidationError('La «Descripción» de la llave puede tener como mucho 255 caracteres.')

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
