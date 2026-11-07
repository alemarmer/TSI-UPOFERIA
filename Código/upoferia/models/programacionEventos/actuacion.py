from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Actuacion(models.Model):
    _name = 'upoferia.actuacion'
    _description = 'Upoferia.actuacion'
    _inherits = {'upoferia.evento': 'evento_id'}
    _sql_constraints = [
        ('evento_uniq', 'UNIQUE ("evento_id")', 'Ese evento ya está registrado como actuación.'),
        ]

    fCache_pactado = fields.Float(string='Caché pactado')

    evento_id = fields.Many2one('upoferia.evento', string='Evento', required=True, ondelete='cascade')

    transaccion_id = fields.Many2one('upoferia.transaccion', string='Contrato', ondelete='set null')

    servicio_ids = fields.Many2many('feria.servicio', 'upoferia_actuacion_servicio', 'actuacion_id', 'servicio_id', string='Servicios')

    artista_ids = fields.Many2many('upoferia.artista', 'upoferia_actuacion_artista',
                                   'actuacion_id', 'artista_id', string='Artistas')

    @api.constrains('fCache_pactado')
    def _check_fCache_pactado(self):
        for record in self:
            if record.fCache_pactado < 0:
                raise ValidationError('«Caché pactado» no puede ser menor que 0.')

    @api.constrains('transaccion_id')
    def _check_transaccion(self):
        for record in self:
            if record.transaccion_id and record.transaccion_id.tipo_transaccion_id.sCodigo != 'CON':
                raise ValidationError('Una actuación solo se puede asociar a un contrato (CON).')
