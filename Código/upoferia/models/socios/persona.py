# -*- coding: utf-8 -*-

import re
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
    registro_accesos_ids = fields.One2many('upoferia.control_accesos.registro_accesos', 'persona_id', string='Registros de accesos')
    
    @api.constrains('dni')
    def _check_dni(self):
        LETRAS_DNI = "TRWAGMYFPDXBNJZSQVHLCKE"
        if not re.match(r"^\d{8}[A-Z]$", self.dni):
            raise models.ValidationError('El DNI debe tener 8 números y una letra.')
        elif LETRAS_DNI[int(self.dni[:8]) % 23] != self.dni[8]:
            raise models.ValidationError("La letra del DNI no es válida.")
            
    @api.constrains('telefono')
    def _check_telefono(self):
        if not self.telefono.isdigit():
            raise models.ValidationError('El teléfono solo debe contener números.')
            
    @api.constrains('email')
    def _check_email(self):
        if self.email and not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", self.email):
            raise models.ValidationError('El correo no es válido.')
            
    _sql_constraints = [('dni_unique', 'UNIQUE(dni)', 'Ya existe un registro con este DNI.')]