from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Concurso(models.Model):
    _name = 'upoferia.concurso'
    _description = 'Upoferia.Concurso'

    sBases = fields.Text(string='Bases')
    dFecha_resultado = fields.Date(string='Fecha del resultado')
    # Lista cerrada según el E-R (Selection): valores por acordar en el grupo
    sEstado = fields.Char(string='Estado')

    @api.constrains('sEstado')
    def _check_longitud(self):
        for record in self:
            for campo in ('sEstado',):
                if record[campo] and len(record[campo]) > 100:
                    raise ValidationError(
                        '«%s» no puede superar los 100 caracteres.' % record._fields[campo].string)

    @api.constrains('sBases', 'sEstado')
    def _check_textos_opcionales(self):
        for record in self:
            for campo in ('sBases', 'sEstado'):
                if record[campo] and not record[campo].strip():
                    raise ValidationError(
                        '«%s» no puede contener solo espacios.' % record._fields[campo].string)
