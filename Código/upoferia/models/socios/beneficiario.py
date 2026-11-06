from odoo import models, fields, api
class Beneficiario(models.Model):
    _name = 'upoferia.socios.beneficiario'
    _description = 'Familiares de los socios titulares'
    _inherits = {'upoferia.socios.persona': 'beneficiario_id'}

    beneficiario_id = fields.Many2one('upoferia.socios.persona', string='Persona', required=True, ondelete='cascade')
    parentesco = fields.Char("Parentesco con el socio")
    socio_id = fields.Many2one('upoferia.socios.socio', string='Socio', required=True, ondelete='cascade')