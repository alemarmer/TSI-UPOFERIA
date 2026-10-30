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

    