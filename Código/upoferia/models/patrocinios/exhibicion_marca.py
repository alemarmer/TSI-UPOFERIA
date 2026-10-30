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

    # «Id. exhibición» obligatorio: no vale texto vacío ni solo espacios (básica)
    @api.constrains('sIdExhibicion')
    def _check_id_exhibicion_obligatorio(self):
        oRegistro = None
        for oRegistro in self:
            if not (oRegistro.sIdExhibicion or '').strip():
                raise ValidationError('El campo «Id. exhibición» es obligatorio.')

    # «Fecha de retirada» no puede ser anterior a «Fecha de montaje» (E-R)
    @api.constrains('dFechaMontaje', 'dFechaRetirada')
    def _check_fecha_retirada(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.dFechaMontaje and oRegistro.dFechaRetirada and oRegistro.dFechaRetirada < oRegistro.dFechaMontaje:
                raise ValidationError('«Fecha de retirada» no puede ser anterior a «Fecha de montaje».')

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
