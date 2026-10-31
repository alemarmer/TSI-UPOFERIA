from odoo import models,fields,api

class Tipo_evento(models.Model):

    _name='upoferia.tipo_evento' 
    _description='Upoferia.tipo_evento'

    sNombre= fields.Char(string="Nombre del tipo de evento", size=60, required=True) 
    sDescripcion = fields.Text(string="Nombre del tipo de evento", size=100)

