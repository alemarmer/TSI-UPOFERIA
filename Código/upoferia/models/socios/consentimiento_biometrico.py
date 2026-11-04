from odoo import models, fields, api

class ConsentimientoBiometrico(models.Model):
    _name = 'upoferia.socios.consentimiento_biometrico'
    _description = 'Consentimiento biométrico'

    name = fields.Char("DNI del socio",size=9, required=True)
    estado = fields.Boolean("Aprobado", default=False)
    fecha_firma = fields.Date("Fecha de firma", autodate=True)
    fecha_renovacion = fields.Date("Fecha de renovación")
    datos_biometricos = fields.Json(string="Datos Biométricos")