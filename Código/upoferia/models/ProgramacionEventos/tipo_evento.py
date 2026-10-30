from odoo import models,fields,api

class tipo_evento(models.Model):

    _name='upoferia.tipo_evento' 
    _description='Tipo de evento'

    sNombre= fields.Char(string="Nombre del tipo de evento", size=60, required=True) 
    sDescripcion = fields.Text(string="Nombre del tipo de evento", size=100)

