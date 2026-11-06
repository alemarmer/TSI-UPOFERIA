from odoo import models, fields, api

class ConsentimientoBiometrico(models.Model):
    _name = 'upoferia.socios.consentimiento_biometrico'
    _description = 'Consentimiento biométrico'

    persona_id = fields.Many2one('upoferia.socios.persona', string='Socio', required=True, ondelete='cascade')
    estado = fields.Boolean("Aprobado", default=False)
    fecha_firma = fields.Date("Fecha de firma", autodate=True)
    fecha_renovacion = fields.Date("Fecha de renovación")
    datos_biometricos = fields.Json(string="Datos Biométricos")