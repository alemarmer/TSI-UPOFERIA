# -*- coding: utf-8 -*-
# Tabla TECNICO del modelo relacional · bloque PATROCINIO Y SERVICIOS
# Subtipo de PERSONA: su clave (dni) es la del supertipo
# y se resolverá con herencia en la fase de relaciones.
#
# Pendiente para la fase de relaciones (no incluido aquí):
#   Validaciones que necesitan claves ajenas:
#     - Un TECNICO es siempre una persona física (necesita la herencia de PERSONA)

from odoo import models, fields


class Tecnico(models.Model):
    _name = 'feria.tecnico'
    _description = 'Técnico'

    # Lista cerrada según el E-R (Selection): valores por acordar en el grupo
    especialidad = fields.Char(string='Especialidad')
    fecha_caducidad_carnet = fields.Date(string='Caducidad del carné')
    cod_carnet_profesional = fields.Char(string='Código del carné profesional')
