from odoo import models,fields,api

class Carruaje(models.Model):
    _name = 'upoferia.carruaje'
    _description = 'Upoferia.carruaje'

    sNum_registro = fields.Char(string='Número de registro', required=True)
    sModelo = fields.Char(string='Modelo')
    iPlazas = fields.Integer(string='Plazas')