from odoo import models, fields, api

class Fichaje(models.Model):
    _name = 'upoferia.turnos.fichaje'
    _description = 'Fichaje de un trabajador'

    id_evento_puerta = fields.Integer("ID del evento de puerta", required=True)
    fecha_turno = fields.Date("Fecha del turno")
    referencia_nomina = fields.Char("Referencia a la nomina del trabajador")