# -*- coding: utf-8 -*-

from odoo import models, fields, api
class Persona(models.Model):
    _name = 'upoferia.socios.persona'
    _description = 'Persona'
    
    dni = fields.Char("DNI",9, required=True)
    nombre = fields.Char("Nombre")
    telefono = fields.Char("Teléfono", 9)
    codigo_persona = fields.Char("Código Persona")
    email = fields.Char("Correo")
    direccion_calle = fields.Char("Calle")
    direccion_ciudad = fields.Char("Ciudad")
    direccion_cp = fields.Char("Código Postal")
    
