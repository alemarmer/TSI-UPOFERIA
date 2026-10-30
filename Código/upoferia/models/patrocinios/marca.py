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
