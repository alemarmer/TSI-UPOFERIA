from odoo import models, fields, api

class Socio(models.Model):
    _name = 'upoferia.socio'
    _description = 'Socio de la caseta'
    
    dni = fields.Char("DNI del propietario",9, required=True)
    estado = fields.Char("Estado")
    fecha_firma = fields.Date("Fecha de firma")
    fecha_renovacion = fields.Date("Fecha de renovación")
    datos_biometricos = fields.Json(string="Datos Biométricos")