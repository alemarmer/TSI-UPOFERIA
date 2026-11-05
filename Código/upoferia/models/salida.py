from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Salida(models.Model):
    _name = 'upoferia.salida'
    _description = 'Upoferia.salida_carruaje'
    _rec_name = 'dFecha_hora_salida'
    _sql_constraints = [
        ('carruaje_fecha_uniq', 'UNIQUE (carruaje_id, dFecha_hora_salida)',
         'Ese carruaje ya tiene una salida a esa fecha y hora.'),
    ]

    
    dFecha_hora_salida = fields.Datetime(string='Fecha y hora de salida', required=True)
    dFecha_hora_vuelta = fields.Datetime(string='Fecha y hora de vuelta')
    iNum_pasajeros = fields.Integer(string='Número de pasajeros')
    # Lista cerrada según el E-R (Selection): valores por acordar en el grupo
    sEstado = fields.Char(string='Estado')

    carruaje_id = fields.Many2one('upoferia.carruaje', string='Carruaje',
                                  required=True, ondelete='cascade')

    #CONEXION CON TRANSACCION

    @api.constrains('dFecha_hora_salida', 'dFecha_hora_vuelta')
    def _check_dFecha_hora_vuelta(self):
        for record in self:
            if record.dFecha_hora_salida and record.dFecha_hora_vuelta and record.dFecha_hora_vuelta <= record.dFecha_hora_salida:
                raise ValidationError('«Fecha y hora de vuelta» debe ser posterior a «Fecha y hora de salida».')

    @api.constrains('iNum_pasajeros')
    def _check_iNum_pasajeros(self):
        for record in self:
            if record.iNum_pasajeros < 0:
                raise ValidationError('«Número de pasajeros» no puede ser menor que 0.')

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

    @api.onchange('dFecha_hora_salida', 'dFecha_hora_vuelta')
    def _onchange_valores(self):
        mensaje = False
        if self.dFecha_hora_salida and self.dFecha_hora_vuelta and self.dFecha_hora_vuelta <= self.dFecha_hora_salida:
            mensaje = '«Fecha y hora de vuelta» debe ser posterior a «Fecha y hora de salida».'
        if mensaje:
            return {
                'warning': {
                    'title': 'Valores incorrectos',
                    'message': mensaje,
                }
            }
