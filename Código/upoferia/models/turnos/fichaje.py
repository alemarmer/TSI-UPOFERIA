from odoo import models, fields, api

class Fichaje(models.Model):
    _name = 'upoferia.turnos.fichaje'
    _description = 'Fichaje de un trabajador'
    _inherits = {'upoferia.control_accesos.evento_puerta': 'evento_puerta_id'}

    evento_puerta_id = fields.Many2one('upoferia.control_accesos.evento_puerta', string='Evento de puerta', required=True, ondelete='cascade')
    fecha_turno = fields.Date("Fecha del turno")
    referencia_nomina = fields.Char("Referencia a la nomina del trabajador")