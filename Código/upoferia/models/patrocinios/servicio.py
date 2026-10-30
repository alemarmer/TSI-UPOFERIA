# -*- coding: utf-8 -*-
# Tabla SERVICIO del modelo relacional · bloque PATROCINIO Y SERVICIOS
# Validaciones de atributo: implementadas al final de la clase.

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Servicio(models.Model):
    _name = 'feria.servicio'
    _description = 'Servicio'
    _rec_name = 'sCodigo'
    _sql_constraints = [
        ('codigo_uniq', 'UNIQUE ("sCodigo")',
         'Ya existe un servicio con ese código.'),
    ]

    sCodigo = fields.Char(string='Código', required=True)
    # Lista cerrada según el E-R (Selection): valores por acordar en el grupo
    sUnidadFacturacion = fields.Char(string='Unidad de facturación')
    bRequiereTecnico = fields.Boolean(string='Requiere técnico')
    sNombre = fields.Char(string='Nombre')

    # «Código» obligatorio: no vale texto vacío ni solo espacios (básica)
    @api.constrains('sCodigo')
    def _check_codigo_obligatorio(self):
        oRegistro = None
        for oRegistro in self:
            if not (oRegistro.sCodigo or '').strip():
                raise ValidationError('El campo «Código» es obligatorio.')
