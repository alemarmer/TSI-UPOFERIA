from odoo import models, fields, api
class Socio(models.Model):
    _name = 'upoferia.socio'
    _description = 'Socio de la caseta'
    
    dni = fields.Char("DNI",9, required=True)
    tipo_socio = fields.Char("Tipo de socio")
    Clan = fields.Char("Clan del socio")