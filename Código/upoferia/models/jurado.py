from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Jurado(models.Model):
    _name = 'upoferia.jurado'
    _description = 'Upoferia.jurado'

    sRol = fields.Char(string='Rol')

    concurso_id = fields.Many2one('upoferia.concurso', string='Concurso',
                                  required=True, ondelete='cascade')

    #FALTA CONEXION CON PERSONA

    @api.constrains('sRol')
    def _check_longitud(self):
        for record in self:
            for campo in ('sRol',):
                if record[campo] and len(record[campo]) > 100:
                    raise ValidationError(
                        '«%s» no puede superar los 100 caracteres.' % record._fields[campo].string)

    @api.constrains('sRol')
    def _check_textos_opcionales(self):
        for record in self:
            for campo in ('sRol',):
                if record[campo] and not record[campo].strip():
                    raise ValidationError(
                        '«%s» no puede contener solo espacios.' % record._fields[campo].string)
