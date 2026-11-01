# -*- coding: utf-8 -*-
# Tabla PROVEEDOR del modelo relacional · bloque PROVEEDORES Y CONTRATOS
# Subtipo de PERSONA: su clave (dni) es la del supertipo
# y se resolverá con herencia en la fase de relaciones.
# Validaciones de atributo: implementadas al final de la clase.

import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Proveedor(models.Model):
    _name = 'feria.proveedor'
    _description = 'Proveedor'
    _sql_constraints = [
        ('cif_uniq', 'UNIQUE (cif)',
         'Ya existe un proveedor con ese CIF.'),
    ]

    # Único; solo se rellena si el proveedor es una empresa (E-R)
    cif = fields.Char(string='CIF')

    # Formato de «CIF» (básica)
    @api.constrains('cif')
    def _check_cif_formato(self):
        for record in self:
            if record.cif and not re.fullmatch(r'[ABCDEFGHJNPQRSUVW][0-9]{7}[0-9A-J]', record.cif):
                raise ValidationError('El CIF debe tener una letra, 7 dígitos y un carácter de control (por ejemplo B12345678).')
