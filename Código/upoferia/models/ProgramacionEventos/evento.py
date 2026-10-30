from odoo import models,fields,api

class evento(models.Model):

    _name='upoferia.evento' #ojo con las minusculas, q se tiene q llamar igual
    _description='Evento'



    sName= fields.Char(string="nombre", size=60, required=True) #obligatorio para todas las clases de python, y simula la pk. odoo por dentro lo hace pk. Si la pk es dni, se cambia en string no en el nombre
    
