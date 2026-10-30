# -*- coding: utf-8 -*-
# Tabla EXHIBICION_MARCA del modelo relacional · bloque PATROCINIO Y SERVICIOS
# Validaciones de atributo: implementadas al final de la clase.
#
# Pendiente para la fase de relaciones (no incluido aquí):
#   Claves ajenas:
#     - nombre_marca -> MARCA (opcional)
#     - dni_tecnico -> TECNICO (opcional)
#     - codigo_lugar_espacio_publicitario -> ESPACIO_PUBLICITARIO (opcional)
#   Atributos derivados (campos compute):
#     - estado (se calcula con las fechas, no se guarda)
#   Validaciones que necesitan claves ajenas:
#     - No se solapa con otra exhibición del mismo ESPACIO_PUBLICITARIO (necesita la FK)

import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ExhibicionMarca(models.Model):
    _name = 'feria.exhibicion_marca'
    _description = 'Exhibición de marca'
    _rec_name = 'sIdExhibicion'
    _sql_constraints = [
        ('id_exhibicion_uniq', 'UNIQUE ("sIdExhibicion")',
         'Ya existe una exhibición con ese identificador.'),
    ]

    # Clave artificial del E-R (Odoo crea además su propio id)
    sIdExhibicion = fields.Char(string='Id. exhibición', required=True)
    dFechaMontaje = fields.Date(string='Fecha de montaje')
    # En el UML es String; si debe guardar el fichero, cambiar a fields.Binary
    sArteFinal = fields.Char(string='Arte final')
    dFechaRetirada = fields.Date(string='Fecha de retirada')

    # «Id. exhibición»: obligatorio, de 2 a 20 caracteres y con formato de código
    # en mayúsculas (letras y números separados por - / . _)
    @api.constrains('sIdExhibicion')
    def _check_id_exhibicion(self):
        oRegistro = None
        sId = ''
        for oRegistro in self:
            sId = oRegistro.sIdExhibicion or ''
            if not sId.strip():
                raise ValidationError('El campo «Id. exhibición» es obligatorio.')
            if not 2 <= len(sId) <= 20:
                raise ValidationError(
                    'El «Id. exhibición» debe tener entre 2 y 20 caracteres.')
            if not re.fullmatch(r'[A-Z0-9]+([-/._][A-Z0-9]+)*', sId):
                raise ValidationError(
                    'El «Id. exhibición» solo puede tener letras mayúsculas y '
                    'números, separados por - / . _ y sin espacios '
                    '(por ejemplo EXH-2026-01).')

    # «Fecha de montaje»: no más de dos años por delante de hoy (criterio propio)
    @api.constrains('dFechaMontaje')
    def _check_fecha_montaje(self):
        oRegistro = None
        dHoy = fields.Date.context_today(self)
        for oRegistro in self:
            if oRegistro.dFechaMontaje and (oRegistro.dFechaMontaje - dHoy).days > 730:
                raise ValidationError(
                    'La «Fecha de montaje» no puede ser más de dos años '
                    'posterior a hoy.')

    # «Fecha de retirada»: necesita fecha de montaje, no puede ser anterior a ella
    # (E-R) y la exhibición no puede durar más de un año (criterio propio)
    @api.constrains('dFechaMontaje', 'dFechaRetirada')
    def _check_fecha_retirada(self):
        oRegistro = None
        for oRegistro in self:
            if not oRegistro.dFechaRetirada:
                continue
            if not oRegistro.dFechaMontaje:
                raise ValidationError(
                    'No se puede indicar la «Fecha de retirada» sin la '
                    '«Fecha de montaje».')
            if oRegistro.dFechaRetirada < oRegistro.dFechaMontaje:
                raise ValidationError('«Fecha de retirada» no puede ser anterior a «Fecha de montaje».')
            if (oRegistro.dFechaRetirada - oRegistro.dFechaMontaje).days > 365:
                raise ValidationError(
                    'Una exhibición no puede durar más de un año entre el '
                    'montaje y la retirada.')

    # Aviso inmediato en el formulario, antes de guardar (como el onchange de gym_2)
    @api.onchange('dFechaMontaje', 'dFechaRetirada')
    def _onchange_valores(self):
        sMensaje = False
        if self.dFechaMontaje and self.dFechaRetirada and self.dFechaRetirada < self.dFechaMontaje:
            sMensaje = '«Fecha de retirada» no puede ser anterior a «Fecha de montaje».'
        if sMensaje:
            return {
                'warning': {
                    'title': 'Valores incorrectos',
                    'message': sMensaje,
                }
            }
