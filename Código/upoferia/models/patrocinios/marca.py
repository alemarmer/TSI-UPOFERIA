import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Marca(models.Model):
    _name = 'upoferia.marca'
    _description = 'Marca'
    _rec_name = 'sNombre'
    _sql_constraints = [
        ('nombre_uniq', 'UNIQUE ("sNombre")',
         'Ya existe una marca con ese nombre.'),
    ]

    sNombre = fields.Char(string='Nombre', required=True)
    binLogotipo = fields.Image(string='Logotipo', max_width=512, max_height=512)
    sColorCorporativo = fields.Char(string='Color corporativo')

    proveedor_id = fields.Many2one('upoferia.proveedor', string='Proveedor', ondelete='set null')
    exhibicion_ids = fields.One2many('upoferia.exhibicion_marca', 'marca_id', string='Exhibiciones')
    patrocinio_ids = fields.One2many('upoferia.patrocinio', 'marca_id', string='Patrocinios')
    producto_ids = fields.One2many('upoferia.producto', 'marca_id', string='Productos')
    
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

    @api.constrains('sColorCorporativo')
    def _check_color_corporativo(self):
        oRegistro = None
        sColor = ''
        for oRegistro in self:
            sColor = oRegistro.sColorCorporativo or ''
            if sColor and not re.fullmatch(
                    r'#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})', sColor):
                raise ValidationError('El color corporativo debe estar en hexadecimal, con el formato #RRGGBB o #RGB (por ejemplo #E30613).')
