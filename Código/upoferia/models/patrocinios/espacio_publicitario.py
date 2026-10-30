# -*- coding: utf-8 -*-
# Tabla ESPACIO_PUBLICITARIO del modelo relacional · bloque PATROCINIO Y SERVICIOS
# Validaciones de atributo: implementadas al final de la clase.
#
# Pendiente para la fase de relaciones (no incluido aquí):
#   Claves ajenas:
#     - nombre_caseta, nombre_zona_caseta -> ZONA_CASETA (opcional)
#   Atributos derivados (campos compute):
#     - fSuperficieM2 = fAnchoM x fAltoM

import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EspacioPublicitario(models.Model):
    _name = 'feria.espacio_publicitario'
    _description = 'Espacio publicitario'
    _rec_name = 'sCodigoLugar'
    _sql_constraints = [
        ('codigo_lugar_uniq', 'UNIQUE ("sCodigoLugar")',
         'Ya existe un espacio publicitario con ese código.'),
    ]

    sCodigoLugar = fields.Char(string='Código del lugar', required=True)
    fAltoM = fields.Float(string='Alto (m)')
    # Lista cerrada según el E-R (Selection): valores por acordar en el grupo
    sTipo = fields.Char(string='Tipo')
    sUbicacionExacta = fields.Char(string='Ubicación exacta')
    fAnchoM = fields.Float(string='Ancho (m)')
    bIluminado = fields.Boolean(string='Iluminado')

    # «Código del lugar»: obligatorio, de 2 a 20 caracteres y con formato de
    # código en mayúsculas (letras y números separados por - / . _)
    @api.constrains('sCodigoLugar')
    def _check_codigo_lugar(self):
        oRegistro = None
        sCodigo = ''
        for oRegistro in self:
            sCodigo = oRegistro.sCodigoLugar or ''
            if not sCodigo.strip():
                raise ValidationError('El campo «Código del lugar» es obligatorio.')
            if not 2 <= len(sCodigo) <= 20:
                raise ValidationError(
                    'El «Código del lugar» debe tener entre 2 y 20 caracteres.')
            if not re.fullmatch(r'[A-Z0-9]+([-/._][A-Z0-9]+)*', sCodigo):
                raise ValidationError(
                    'El «Código del lugar» solo puede tener letras mayúsculas y '
                    'números, separados por - / . _ y sin espacios '
                    '(por ejemplo PORTADA-01).')

    # «Alto (m)»: mayor que 0, como mucho 30 m y con precisión de centímetros
    @api.constrains('fAltoM')
    def _check_alto_m(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.fAltoM <= 0:
                raise ValidationError('«Alto (m)» debe ser mayor que 0.')
            if oRegistro.fAltoM > 30:
                raise ValidationError('«Alto (m)» no puede superar los 30 metros.')
            if round(oRegistro.fAltoM, 2) != oRegistro.fAltoM:
                raise ValidationError(
                    '«Alto (m)» solo admite dos decimales (centímetros).')

    # «Ancho (m)»: mayor que 0, como mucho 30 m y con precisión de centímetros
    @api.constrains('fAnchoM')
    def _check_ancho_m(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.fAnchoM <= 0:
                raise ValidationError('«Ancho (m)» debe ser mayor que 0.')
            if oRegistro.fAnchoM > 30:
                raise ValidationError('«Ancho (m)» no puede superar los 30 metros.')
            if round(oRegistro.fAnchoM, 2) != oRegistro.fAnchoM:
                raise ValidationError(
                    '«Ancho (m)» solo admite dos decimales (centímetros).')
