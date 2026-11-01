# -*- coding: utf-8 -*-
# Tabla CATEGORIA_PROVEEDOR del modelo relacional · bloque PROVEEDORES Y CONTRATOS
# Validaciones de atributo: implementadas al final de la clase.
#
# Pendiente para la fase de relaciones (no incluido aquí):
#   Claves ajenas:
#     - nombre_padre -> CATEGORIA_PROVEEDOR (opcional, reflexiva)
#   Validaciones que necesitan claves ajenas:
#     - No puede ser subcategoría de sí misma ni formar ciclos (en Odoo 18: _has_cycle)

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
    sColor = fields.Char(string='Color')

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
