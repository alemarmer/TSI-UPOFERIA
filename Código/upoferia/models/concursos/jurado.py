from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Jurado(models.Model):
    _name = 'upoferia.jurado'
    _description = 'Upoferia.jurado'

    sRol = fields.Selection([('presidente', 'Presidente'),
                            ('vocal', 'Vocal'),
                            ('secretario', 'Secretario')],
                           string='Rol')

    concurso_id = fields.Many2one('upoferia.concurso', string='Concurso',
                                  required=True, ondelete='cascade')

    #FALTA CONEXION CON PERSONA

