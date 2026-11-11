from odoo import models, fields, api
class Socio(models.Model):
    _name = 'upoferia.socios.socio'
    _description = 'Socio de la caseta'
    _inherits = {'upoferia.socios.persona': 'persona_id'}

    persona_id = fields.Many2one('upoferia.socios.persona', string='DNI', required=True, ondelete='cascade')
    tipo_socio_id = fields.Many2one('upoferia.socios.tipo_socio', string="Tipo de socio", required=True)
    invitaciones_ids = fields.One2many('upoferia.socios.invitacion_acceso', 'socio_id', string="Invitaciones")
    beneficiarios_ids = fields.One2many('upoferia.socios.beneficiario', 'socio_id', string="Beneficiarios")
    clan = fields.Char("Clan del socio")