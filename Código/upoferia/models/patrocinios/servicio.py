# -*- coding: utf-8 -*-
# Tabla SERVICIO del modelo relacional · bloque PATROCINIO Y SERVICIOS
# Validaciones de atributo: implementadas al final de la clase.

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Servicio(models.Model):
    _name = 'feria.servicio'
    _description = 'Servicio'
    _rec_name = 'codigo'
    _sql_constraints = [
        ('codigo_uniq', 'UNIQUE (codigo)',
         'Ya existe un servicio con ese código.'),
    ]

    codigo = fields.Char(string='Código', required=True)
    # Lista cerrada según el E-R (Selection): valores por acordar en el grupo
    unidad_facturacion = fields.Char(string='Unidad de facturación')
    requiere_tecnico = fields.Boolean(string='Requiere técnico')
    nombre = fields.Char(string='Nombre')

    # «Código» obligatorio: no vale texto vacío ni solo espacios (básica)
    @api.constrains('codigo')
    def _check_codigo_obligatorio(self):
        for record in self:
            if not (record.codigo or '').strip():
                raise ValidationError('El campo «Código» es obligatorio.')
