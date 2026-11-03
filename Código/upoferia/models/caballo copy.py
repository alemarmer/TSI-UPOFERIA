from odoo import models,fields,api

class Caballo(models.Model):

    _name='upoferia.caballo' 
    _description='Upoferia.caballo'

    sMicrochip= fields.Char(string="Microchip del caballo", size=60, required=True) 
    sNombre = fields.Char(string="Nombre del caballo", size=100)
    sRaza = fields.Char(string="Raza del caballo", size=100)
    sSexo = fields.Char(string="Sexo del caballo", size=100)
