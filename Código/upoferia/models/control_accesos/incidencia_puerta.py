from odoo import models, fields, api

class IncidenciaPuerta(models.Model):
    _name = 'upoferia.control_accesos.incidencia_puerta'
    _description = 'Incidencia de puerta'

    name = fields.Integer("ID del evento de puerta", required=True)
    motivo = fields.Char("Motivo")
    