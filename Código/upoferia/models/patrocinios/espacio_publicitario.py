# -*- coding: utf-8 -*-
# Tabla ESPACIO_PUBLICITARIO del modelo relacional · bloque PATROCINIO Y SERVICIOS
# Validaciones de atributo: implementadas al final de la clase.
#
# Pendiente para la fase de relaciones (no incluido aquí):
#   Claves ajenas:
#     - nombre_caseta, nombre_zona_caseta -> ZONA_CASETA (opcional)
#   Atributos derivados (campos compute):
#     - superficie_m2 = ancho_m x alto_m

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

    # «Código del lugar» obligatorio: no vale texto vacío ni solo espacios (básica)
    @api.constrains('sCodigoLugar')
    def _check_codigo_lugar_obligatorio(self):
        oRegistro = None
        for oRegistro in self:
            if not (oRegistro.sCodigoLugar or '').strip():
                raise ValidationError('El campo «Código del lugar» es obligatorio.')

    # «Alto (m)» debe ser mayor que 0 (básica)
    @api.constrains('fAltoM')
    def _check_alto_m(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.fAltoM <= 0:
                raise ValidationError('«Alto (m)» debe ser mayor que 0.')

    # «Ancho (m)» debe ser mayor que 0 (básica)
    @api.constrains('fAnchoM')
    def _check_ancho_m(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.fAnchoM <= 0:
                raise ValidationError('«Ancho (m)» debe ser mayor que 0.')
