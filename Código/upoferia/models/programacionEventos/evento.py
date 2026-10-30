from odoo import models,fields,api

class Evento(models.Model):

    _name='upoferia.evento' 
    _description='Evento'

    sNombre= fields.Char(string="Nombre del evento", size=60, required=True) #obligatorio para todas las clases de python, y simula la pk. odoo por dentro lo hace pk. Si la pk es dni, se cambia en string no en el nombre
    dFecha_hora_inicio = fields.Datetime(string='Fecha y hora de inicio')
    dFecha_hora_fin = fields.Datetime(string='Fecha y hora de finalizacion')
    iAforo_reservado = fields.Integer(string='Aforo reservado')
    sEstado = fields.Char(string='Estado')

