# -*- coding: utf-8 -*-
# Tabla MARCA del modelo relacional · bloque PATROCINIO Y SERVICIOS
#
# Pendiente:
# Claves ajenas:
#     - dni_proveedor -> PROVEEDOR (opcional)

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Marca(models.Model):
    _name = 'feria.marca'
    _description = 'Marca'
    _rec_name = 'sNombre'
    _sql_constraints = [
        ('nombre_uniq', 'UNIQUE ("sNombre")',
         'Ya existe una marca con ese nombre.'),
    ]

    sNombre = fields.Char(string='Nombre', required=True)
    sLogotipo = fields.Char(string='Logotipo')
    sColorCorporativo = fields.Char(string='Color corporativo')

    @api.constrains('sNombre')
    def _check_nombre_obligatorio(self):
        oRegistro = None
        for oRegistro in self:
            if not (oRegistro.sNombre or '').strip():
                raise ValidationError('El campo «Nombre» es obligatorio.')

    @api.constrains('sNombre')
    def _check_nombre_espacios(self):
        oRegistro = None
        sNombre = ''
        for oRegistro in self:
            sNombre = oRegistro.sNombre or ''
            if sNombre != sNombre.strip():
                raise ValidationError(
                    'El nombre de la marca no puede empezar ni terminar '
                    'con espacios.')
            if '  ' in sNombre:
                raise ValidationError(
                    'El nombre de la marca no puede tener dos espacios '
                    'seguidos.')

    @api.constrains('sNombre')
    def _check_nombre_longitud(self):
        oRegistro = None
        iLongitud = 0
        for oRegistro in self:
            iLongitud = len((oRegistro.sNombre or '').strip())
            if iLongitud and not 2 <= iLongitud <= 100:
                raise ValidationError(
                    'El nombre de la marca debe tener entre 2 y 100 '
                    'caracteres.')
