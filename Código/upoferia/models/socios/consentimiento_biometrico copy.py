from odoo import models, fields, api

class ConsentimientoBiometrico(models.Model):
    _name = 'upoferia.socios.consentimiento_biometrico'
    _description = 'Consentimiento biométrico'

    socio_dni = fields.Char("DNI del socio",9, required=True)
    estado = fields.Char("Estado")
    fecha_firma = fields.Date("Fecha de firma")
    fecha_renovacion = fields.Date("Fecha de renovación")
    datos_biometricos = fields.Json(string="Datos Biométricos")