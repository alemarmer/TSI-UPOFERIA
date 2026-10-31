from odoo import models, fields, api
class Beneficiario(models.Model):
    _name = 'upoferia.socios.beneficiario'
    _description = 'Familiares de los socios titulares'

    name = fields.Char("DNI", size=9, required=True)
    parentesco = fields.Char("Parentesco con el socio")
    name2 = fields.Char("DNI del socio titular", size=9, required=True)