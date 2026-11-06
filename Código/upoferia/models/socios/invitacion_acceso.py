from odoo import models, fields, api
class InvitacionAcceso(models.Model):
    _name = 'upoferia.socios.invitacion_acceso'
    _description = 'Invitación de acceso'

    socio_id = fields.Many2one('upoferia.socios.persona', string='Socio', required=True, ondelete='cascade')
    persona_id = fields.Many2one('upoferia.socios.persona', string='Invitado', required=True, ondelete='cascade')
    fecha_validez = fields.Date("Fecha de validez", autodate=True)