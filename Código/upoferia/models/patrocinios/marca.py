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
    def _check_nombre(self):
        oRegistro = None
        sNombre = ''
        oMarca = None
        for oRegistro in self:
            sNombre = oRegistro.sNombre or ''
            if not sNombre.strip():
                raise ValidationError('El campo «Nombre» es obligatorio.')
            if sNombre != sNombre.strip():
                raise ValidationError('El nombre de la marca no puede empezar ni terminar con espacios.')
            if not 2 <= len(sNombre) <= 100:
                raise ValidationError('El nombre de la marca debe tener entre 2 y 100 caracteres.')
            for oMarca in self.search([('sNombre', 'ilike', sNombre), ('id', '!=', oRegistro.id)]):
                if oMarca.sNombre.lower() == sNombre.lower():
                    raise ValidationError('Ya existe una marca llamada «%s» (aunque esté escrita con otras mayúsculas).' % oMarca.sNombre)

    @api.constrains('sLogotipo')
    def _check_logotipo(self):
        oRegistro = None
        sLogotipo = ''
        for oRegistro in self:
            sLogotipo = oRegistro.sLogotipo or ''
            if ' ' in sLogotipo:
                raise ValidationError('El logotipo no puede tener espacios.')
            if len(sLogotipo) > 255:
                raise ValidationError('El logotipo no puede tener más de 255 caracteres.')
            if sLogotipo and not re.fullmatch(r'(?i)https?://\S+|\S+\.(png|jpe?g|svg|webp)', sLogotipo):
                raise ValidationError('El logotipo debe ser una URL que empiece por http:// o https://, o un archivo .png, .jpg, .jpeg, .svg o .webp.')

    @api.constrains('sColorCorporativo')
    def _check_color_corporativo(self):
        oRegistro = None
        sColor = ''
        for oRegistro in self:
            sColor = oRegistro.sColorCorporativo or ''
            if sColor and not re.fullmatch(
                    r'#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})', sColor):
                raise ValidationError('El color corporativo debe estar en hexadecimal, con el formato #RRGGBB o #RGB (por ejemplo #E30613).')
