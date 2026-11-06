from odoo import models, fields, api

class EventoPuerta(models.Model):
    _name = 'upoferia.control_accesos.evento_puerta'
    _description = 'Evento de puerta'
    _rec_name = 'evento_puerta_id'

    evento_puerta_id = fields.Integer("ID del evento de puerta", required=True)
    