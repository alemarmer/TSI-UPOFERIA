from odoo import models, fields, api
class InvitacionAcceso(models.Model):
    _name = 'upoferia.socios.invitacion_acceso'
    _description = 'Invitación de acceso'

    socio_id = fields.Many2one('upoferia.socios.persona', string='Socio', required=True, ondelete='cascade')
    persona_id = fields.Many2one('upoferia.socios.persona', string='Invitado', required=True, ondelete='cascade')
    fecha_validez = fields.Date("Fecha de validez", autodate=True)
    
    @api.constrains('fecha_validez')
    def _check_fecha_validez(self):
        if self.fecha_validez and self.fecha_validez < fields.Date.today():
            raise models.ValidationError('La fecha de validez no puede ser anterior a la fecha actual.')