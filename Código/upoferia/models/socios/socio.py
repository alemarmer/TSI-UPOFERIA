from odoo import models, fields, api
class Socio(models.Model):
    _name = 'upoferia.socios.socio'
    _description = 'Socio de la caseta'
    
    name = fields.Char("DNI",size=9, required=True)
    tipo_socio = fields.Char("Tipo de socio")
    clan = fields.Char("Clan del socio")