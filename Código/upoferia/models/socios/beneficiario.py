from odoo import models, fields, api
class Beneficiario(models.Model):
    _name = 'upoferia.socios.beneficiario'
    _description = 'Familiares de los socios titulares'
    _inherits = {'upoferia.socios.persona': 'beneficiario_id'}

    beneficiario_id = fields.Many2one('upoferia.socios.persona', string='Persona', required=True, ondelete='cascade')
    parentesco = fields.Selection(selection=[('padre', 'Padre'), ('madre', 'Madre'), ('hijo', 'Hijo'), ('hija', 'Hija'), ('hermano', 'Hermano'), ('hermana', 'Hermana'), ('familiar_segundo_grado', 'Familiar de segundo grado'), ('otro', 'Otro')], string="Parentesco con el socio")
    socio_id = fields.Many2one('upoferia.socios.socio', string='Socio', required=True, ondelete='cascade')