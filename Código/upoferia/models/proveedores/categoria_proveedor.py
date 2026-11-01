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

    # «Nombre» obligatorio: no vale texto vacío ni solo espacios (básica)
    @api.constrains('sNombre')
    def _check_nombre_obligatorio(self):
        oRegistro = None
        for oRegistro in self:
            if not (oRegistro.sNombre or '').strip():
                raise ValidationError('El campo «Nombre» es obligatorio.')
