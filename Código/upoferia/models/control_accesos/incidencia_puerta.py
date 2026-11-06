from odoo import models, fields, api

class IncidenciaPuerta(models.Model):
    _name = 'upoferia.control_accesos.incidencia_puerta'
    _description = 'Incidencia de puerta'
    _inherits = {'upoferia.control_accesos.evento_puerta': 'evento_puerta_id'}

    evento_puerta_id = fields.Many2one('upoferia.control_accesos.evento_puerta', string='Evento de puerta', required=True, ondelete='cascade')
    motivo = fields.Char("Motivo")
    