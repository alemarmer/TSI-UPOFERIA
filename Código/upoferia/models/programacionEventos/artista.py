from odoo import models,fields,api

class Artista(models.Model):
    _name = 'upoferia.artista'
    _description = 'Upoferia.artista'

    sDni= fields.Char(string="DNI del artista", size=60, required=True)
    fCache_base = fields.Float(string='Caché base')
    sMontaje = fields.Char(string='Montaje')
    sIluminacion = fields.Char(string='Iluminación')
    fPotencia_kw = fields.Float(string='Potencia (kW)')
    sSonido = fields.Char(string='Sonido')
    sEspacio = fields.Char(string='Espacio')