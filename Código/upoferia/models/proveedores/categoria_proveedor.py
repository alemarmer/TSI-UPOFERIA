from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CategoriaProveedor(models.Model):
    _name = 'feria.categoria_proveedor'
    _description = 'Categoría de proveedor'
    _rec_name = 'sNombre'
    _sql_constraints = [
        ('nombre_uniq', 'UNIQUE ("sNombre")',
         'Ya existe una categoría de proveedor con ese nombre.'),
    ]

    sNombre = fields.Char(string='Nombre', required=True)
    iColor = fields.Integer(string='Color', default=0)

    padre_id = fields.Many2one('feria.categoria_proveedor', string='Categoría padre', ondelete='restrict')
    hija_ids = fields.One2many('feria.categoria_proveedor', 'padre_id', string='Subcategorías')
    proveedor_ids = fields.Many2many('feria.proveedor', 'feria_proveedor_categoria_rel', 'categoria_proveedor_id', 'proveedor_id', string='Proveedores')

    @api.constrains('sNombre')
    def _check_nombre(self):
        oRegistro = None
        sNombre = ''
        oCategoria = None
        for oRegistro in self:
            sNombre = oRegistro.sNombre or ''
            if not sNombre.strip():
                raise ValidationError('El campo «Nombre» es obligatorio.')
            if sNombre != sNombre.strip():
                raise ValidationError('El nombre de la categoría no puede empezar ni terminar con espacios.')
            if not 2 <= len(sNombre) <= 50:
                raise ValidationError('El nombre de la categoría debe tener entre 2 y 50 caracteres.')
            for oCategoria in self.search([('sNombre', 'ilike', sNombre), ('id', '!=', oRegistro.id)]):
                if oCategoria.sNombre.lower() == sNombre.lower():
                    raise ValidationError('Ya existe una categoría llamada «%s» (aunque esté escrita con otras mayúsculas).' % oCategoria.sNombre)

    @api.constrains('iColor')
    def _check_color(self):
        oRegistro = None
        for oRegistro in self:
            if not 0 <= oRegistro.iColor <= 11:
                raise ValidationError('El color de la categoría debe ser un número entre 0 y 11 (los colores de las etiquetas de Odoo).')
