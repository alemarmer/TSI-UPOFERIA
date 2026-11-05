from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Reserva(models.Model):
    _name = 'upoferia.reserva'
    _description = 'Upoferia.reserva'

    dHora_llegada = fields.Datetime(string='Hora de llegada', required=True)
    iNum_personas = fields.Integer(string='Número de personas')
    sEstado = fields.Char(string='sEstado')

    #MANY2ONE CON MESA (OJO ES TAMBIEN PK)
    #MANY2ONE CON SOCIO

    @api.constrains('iNum_personas')
    def _check_iNum_personas(self):
        for record in self:
            if record.iNum_personas <= 0:
                raise ValidationError('«Número de personas» debe ser mayor que 0.')

    @api.constrains('sEstado')
    def _check_longitud(self):
        for record in self:
            for campo in ('sEstado',):
                if record[campo] and len(record[campo]) > 100:
                    raise ValidationError(
                        '«%s» no puede superar los 100 caracteres.' % record._fields[campo].string)

    @api.constrains('sEstado')
    def _check_textos_opcionales(self):
        for record in self:
            for campo in ('sEstado',):
                if record[campo] and not record[campo].strip():
                    raise ValidationError(
                        '«%s» no puede contener solo espacios.' % record._fields[campo].string)



