from odoo import models, fields, api

class EventoPuerta(models.Model):
    _name = 'upoferia.control_accesos.evento_puerta'
    _description = 'Evento de puerta'

    id_evento_puerta = fields.Integer("ID del evento de puerta", required=True)
    