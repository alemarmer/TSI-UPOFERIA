# -*- coding: utf-8 -*-
# Tabla SERVICIO del modelo relacional · bloque PATROCINIO Y SERVICIOS
# Validaciones de atributo: implementadas al final de la clase.

import re

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

    @api.constrains('sCodigo')
    def _check_codigo(self):
        oRegistro = None
        sCodigo = ''
        for oRegistro in self:
            sCodigo = oRegistro.sCodigo or ''
            if not sCodigo.strip():
                raise ValidationError('El campo «Código» es obligatorio.')
            if not 2 <= len(sCodigo) <= 20:
                raise ValidationError('El «Código» del servicio debe tener entre 2 y 20 caracteres.')
            if not re.fullmatch(r'[A-Z0-9]+([-/._][A-Z0-9]+)*', sCodigo):
                raise ValidationError('El «Código» del servicio solo puede tener letras mayúsculas y números, separados por - / . _ y sin espacios (por ejemplo SRV-SONIDO).')
