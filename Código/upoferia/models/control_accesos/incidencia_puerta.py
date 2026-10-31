from odoo import models, fields, api

class ControlAforo(models.Model):
    _name = 'upoferia.control_accesos.control_aforo'
    _description = 'Control de aforo'

    name = fields.Integer("ID del evento de puerta", required=True)
    motivo = fields.Char("Motivo")
    