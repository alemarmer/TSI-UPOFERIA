# Autor: Juanjo (Personal - RRHH y Turnos)
# Versión mínima de Persona para que el módulo de RRHH se instale sin la rama de Socios.
# Mismo _name y campos que la de Ale, sin las relaciones con modelos de socios y control de accesos.
import re
from odoo import models, fields, api


class Persona(models.Model):

    _name = 'upoferia.socios.persona'
    _description = 'Persona'
    _rec_name = 'dni'

    dni = fields.Char(string="DNI", size=9, required=True)
    nombre = fields.Char(string="Nombre")
    telefono = fields.Char(string="Teléfono", size=9)
    codigo_persona = fields.Char(string="Código Persona")
    email = fields.Char(string="Correo")
    direccion_calle = fields.Char(string="Calle")
    direccion_ciudad = fields.Char(string="Ciudad")
    direccion_cp = fields.Char(string="Código Postal")

    _sql_constraints = [
        ('dni_unique', 'UNIQUE(dni)', 'Ya existe un registro con este DNI.'),
    ]

    @api.constrains('dni')
    def _check_dni(self):
        letras_dni = 'TRWAGMYFPDXBNJZSQVHLCKE'
        for record in self:
            if not re.match(r'^\d{8}[A-Z]$', record.dni):
                raise models.ValidationError('El DNI debe tener 8 números y una letra.')
            if letras_dni[int(record.dni[:8]) % 23] != record.dni[8]:
                raise models.ValidationError('La letra del DNI no es válida.')

    @api.constrains('telefono')
    def _check_telefono(self):
        for record in self:
            if record.telefono and not record.telefono.isdigit():
                raise models.ValidationError('El teléfono solo debe contener números.')

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', record.email):
                raise models.ValidationError('El correo no es válido.')
