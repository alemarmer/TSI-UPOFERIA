from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Reserva(models.Model):
    _name = 'upoferia.reserva'
    _description = 'Upoferia.reserva'

    hora_llegada = fields.Datetime(string='Hora de llegada', required=True)
    num_personas = fields.Integer(string='Número de personas')
    estado = fields.Char(string='Estado')

    @api.constrains('num_personas')
    def _check_num_personas(self):
        for record in self:
            if record.num_personas <= 0:
                raise ValidationError('«Número de personas» debe ser mayor que 0.')

    @api.constrains('estado')
    def _check_longitud(self):
        for record in self:
            for campo in ('estado',):
                if record[campo] and len(record[campo]) > 100:
                    raise ValidationError(
                        '«%s» no puede superar los 100 caracteres.' % record._fields[campo].string)

    @api.constrains('estado')
    def _check_textos_opcionales(self):
        for record in self:
            for campo in ('estado',):
                if record[campo] and not record[campo].strip():
                    raise ValidationError(
                        '«%s» no puede contener solo espacios.' % record._fields[campo].string)



