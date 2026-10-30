# -*- coding: utf-8 -*-
# Tabla TECNICO del modelo relacional · bloque PATROCINIO Y SERVICIOS
# Subtipo de PERSONA: su clave (dni) es la del supertipo
# y se resolverá con herencia en la fase de relaciones.
#
# Pendiente para la fase de relaciones (no incluido aquí):
#   Validaciones que necesitan claves ajenas:
#     - Un TECNICO es siempre una persona física (necesita la herencia de PERSONA)

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Tecnico(models.Model):
    _name = 'feria.tecnico'
    _description = 'Técnico'

    # Lista cerrada según el E-R (Selection): valores por acordar en el grupo
    sEspecialidad = fields.Char(string='Especialidad')
    dFechaCaducidadCarnet = fields.Date(string='Caducidad del carné')
    sCodCarnetProfesional = fields.Char(string='Código del carné profesional')

    @api.constrains('sEspecialidad')
    def _check_especialidad(self):
        oRegistro = None
        sEspecialidad = ''
        for oRegistro in self:
            sEspecialidad = oRegistro.sEspecialidad or ''
            if not sEspecialidad:
                continue
            if sEspecialidad != sEspecialidad.strip() or '  ' in sEspecialidad:
                raise ValidationError('La «Especialidad» no puede empezar ni terminar con espacios ni tener dos espacios seguidos.')
            if not 2 <= len(sEspecialidad) <= 50:
                raise ValidationError('La «Especialidad» debe tener entre 2 y 50 caracteres.')
