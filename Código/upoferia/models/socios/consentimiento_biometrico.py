from odoo import models, fields, api

class ConsentimientoBiometrico(models.Model):
    _name = 'upoferia.socios.consentimiento_biometrico'
    _description = 'Consentimiento biométrico'

    persona_id = fields.Many2one('upoferia.socios.persona', string='Socio', required=True, ondelete='cascade')
    estado = fields.Boolean("Aprobado", default=False)
    fecha_firma = fields.Date("Fecha de firma", autodate=True)
    fecha_renovacion = fields.Date("Fecha de renovación")
    datos_biometricos = fields.Binary(string="Datos Biométricos") #Dejo binary de momento, pero se este campo variará de tipo según las necesidades de la libreria usada para el reconocimiento facial.
    
    @api.constrains('fecha_firma')
    def _check_fecha_firma(self):
        if self.fecha_firma and self.fecha_firma < fields.Date.today():
            raise models.ValidationError('La fecha de firma no puede ser anterior a la fecha actual.')

    @api.constrains('fecha_renovacion')
    def _check_fecha_renovacion(self):
        if self.fecha_renovacion and self.fecha_renovacion < fields.Date.today():
            raise models.ValidationError('La fecha de renovación no puede ser anterior a la fecha actual.')