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
    _rec_name = 'id_exhibicion'
    _sql_constraints = [
        ('id_exhibicion_uniq', 'UNIQUE (id_exhibicion)',
         'Ya existe una exhibición con ese identificador.'),
    ]

    # Clave artificial del E-R (Odoo crea además su propio id)
    id_exhibicion = fields.Char(string='Id. exhibición', required=True)
    fecha_montaje = fields.Date(string='Fecha de montaje')
    # En el UML es String; si debe guardar el fichero, cambiar a fields.Binary
    arte_final = fields.Char(string='Arte final')
    fecha_retirada = fields.Date(string='Fecha de retirada')

    # «Id. exhibición» obligatorio: no vale texto vacío ni solo espacios (básica)
    @api.constrains('id_exhibicion')
    def _check_id_exhibicion_obligatorio(self):
        for record in self:
            if not (record.id_exhibicion or '').strip():
                raise ValidationError('El campo «Id. exhibición» es obligatorio.')

    # «Fecha de retirada» no puede ser anterior a «Fecha de montaje» (E-R)
    @api.constrains('fecha_montaje', 'fecha_retirada')
    def _check_fecha_retirada(self):
        for record in self:
            if record.fecha_montaje and record.fecha_retirada and record.fecha_retirada < record.fecha_montaje:
                raise ValidationError('«Fecha de retirada» no puede ser anterior a «Fecha de montaje».')

    # Aviso inmediato en el formulario, antes de guardar (como el onchange de gym_2)
    @api.onchange('fecha_montaje', 'fecha_retirada')
    def _onchange_valores(self):
        mensaje = False
        if self.fecha_montaje and self.fecha_retirada and self.fecha_retirada < self.fecha_montaje:
            mensaje = '«Fecha de retirada» no puede ser anterior a «Fecha de montaje».'
        if mensaje:
            return {
                'warning': {
                    'title': 'Valores incorrectos',
                    'message': mensaje,
                }
            }
