# -*- coding: utf-8 -*-
# Tabla MARCA del modelo relacional · bloque PATROCINIO Y SERVICIOS
#
# Pendiente:
# Claves ajenas:
#     - dni_proveedor -> PROVEEDOR (opcional)

import re

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

    @api.constrains('sNombre')
    def _check_nombre_caracteres(self):
        oRegistro = None
        sNombre = ''
        for oRegistro in self:
            sNombre = (oRegistro.sNombre or '').strip()
            if not sNombre:
                continue
            if not re.fullmatch(r"(?:[^\W_]|[ &'.\-])+", sNombre):
                raise ValidationError(
                    'El nombre de la marca solo puede tener letras, números, '
                    'espacios y los signos & \' . -')
            if not re.search(r'[^\W\d_]', sNombre):
                raise ValidationError(
                    'El nombre de la marca debe tener al menos una letra.')

    @api.constrains('sNombre')
    def _check_nombre_unico(self):
        oRegistro = None
        sNombre = ''
        oParecidas = None
        for oRegistro in self:
            sNombre = (oRegistro.sNombre or '').strip()
            if not sNombre:
                continue
            oParecidas = self.search([
                ('sNombre', 'ilike', sNombre),
                ('id', '!=', oRegistro.id),
            ])
            if any((oParecida.sNombre or '').strip().lower() == sNombre.lower()
                   for oParecida in oParecidas):
                raise ValidationError(
                    'Ya existe una marca con el nombre «%s» (aunque esté '
                    'escrito con otras mayúsculas).' % sNombre)

    @api.constrains('sLogotipo')
    def _check_logotipo(self):
        oRegistro = None
        sLogotipo = ''
        for oRegistro in self:
            sLogotipo = oRegistro.sLogotipo or ''
            if not sLogotipo:
                continue
            if not sLogotipo.strip():
                raise ValidationError(
                    'El logotipo no puede estar formado solo por espacios.')
            if len(sLogotipo) > 255:
                raise ValidationError(
                    'El logotipo no puede tener más de 255 caracteres.')
            if ' ' in sLogotipo:
                raise ValidationError(
                    'El logotipo es una URL o una ruta de archivo y no puede '
                    'tener espacios.')
            if not re.fullmatch(r'(?i)https?://\S+|\S+\.(png|jpe?g|svg|webp)',
                                sLogotipo):
                raise ValidationError(
                    'El logotipo debe ser una URL que empiece por http:// o '
                    'https://, o un archivo .png, .jpg, .jpeg, .svg o .webp.')
