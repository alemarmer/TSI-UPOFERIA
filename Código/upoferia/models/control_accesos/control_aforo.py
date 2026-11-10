from odoo import models, fields, api

class ControlAforo(models.Model):
    _name = 'upoferia.control_accesos.control_aforo'
    _description = 'Control de aforo'
    _inherits = {'upoferia.control_accesos.evento_puerta': 'evento_puerta_id'}

    evento_puerta_id = fields.Many2one('upoferia.control_accesos.evento_puerta', string='Evento de puerta', required=True, ondelete='cascade')
    ocupacion_actual = fields.Integer("Ocupación actual")
    aforo_maximo = fields.Integer("Aforo máximo")
    
    @api.constrains('ocupacion_actual', 'aforo_maximo')
    def _check_aforo(self):
        if self.ocupacion_actual > self.aforo_maximo:
            raise models.ValidationError('La ocupación actual no puede superar el aforo máximo.')