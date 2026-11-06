# -*- coding: utf-8 -*-

from odoo import models, fields, api
class Persona(models.Model):
    _name = 'upoferia.socios.persona'
    _description = 'Persona'
    _rec_name = 'dni'
    
    dni = fields.Char(string="DNI", size=9, required=True)
    nombre = fields.Char("Nombre")
    telefono = fields.Char("Teléfono", size=9)
    codigo_persona = fields.Char("Código Persona")
    email = fields.Char("Correo")
    direccion_calle = fields.Char("Calle")
    direccion_ciudad = fields.Char("Ciudad")
    direccion_cp = fields.Char("Código Postal")
    invitaciones_recibidas_ids = fields.One2many('upoferia.socios.invitacion_acceso', 'persona_id', string="Invitaciones recibidas")
    consentimiento_biometrico_ids = fields.One2many('upoferia.socios.consentimiento_biometrico', 'persona_id', string="Consentimientos biométricos")
    
    _sql_constraints = [('dni_unique', 'UNIQUE(dni)', 'Ya existe un registro con este DNI.')]