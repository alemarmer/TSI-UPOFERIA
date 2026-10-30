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
    _rec_name = 'nombre'
    _sql_constraints = [
        ('nombre_uniq', 'UNIQUE (nombre)',
         'Ya existe una marca con ese nombre.'),
    ]

    nombre = fields.Char(string='Nombre', required=True)
    logotipo = fields.Char(string='Logotipo')
    color_corporativo = fields.Char(string='Color corporativo')

    @api.constrains('nombre')
    def _check_nombre_obligatorio(self):
        for record in self:
            if not (record.nombre or '').strip():
                raise ValidationError('El campo «Nombre» es obligatorio.')
