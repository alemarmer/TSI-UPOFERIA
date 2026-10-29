from odoo import models, fields, api
class Beneficiario(models.Model):
    _name = 'upoferia.socios.beneficiario'
    _description = 'Familiares de los socios titulares'

    dni = fields.Char("DNI",9, required=True)
    parentesco = fields.Char("Parentesco con el socio", required=True)
    socio_dni = fields.Char("DNI del socio titular")