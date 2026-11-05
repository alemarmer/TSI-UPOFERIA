from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Actuacion(models.Model):
    _name = 'upoferia.actuacion'
    _description = 'Upoferia.actuacion'
    sql_constraints = [
        ('evento_uniq', 'UNIQUE (evento_id)', 'Ese evento ya está registrado como actuación.'),
        ]

    fCache_pactado = fields.Float(string='Caché pactado')

    sNombre_evento = fields.Many2one('upoferia.evento', string='Evento', required=True, ondelete='cascade')

    #FK id_transaccion

    @api.constrains('fCache_pactado')
    def _check_fCache_pactado(self):
        for record in self:
            if record.fCache_pactado < 0:
                raise ValidationError('«Caché pactado» no puede ser menor que 0.')