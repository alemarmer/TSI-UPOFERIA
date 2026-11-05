from odoo import models,fields,api
from odoo.exceptions import ValidationError

class Carruaje(models.Model):
    _name = 'upoferia.carruaje'
    _description = 'Upoferia.carruaje'

    sNum_registro = fields.Char(string='Número de registro', required=True)
    sModelo = fields.Char(string='Modelo')
    iPlazas = fields.Integer(string='Plazas')

    salida_ids = fields.One2many('upoferia.salida', 'carruaje_id', string='Salidas')

    @api.constrains('sNum_registro')
    def _check_sNum_registro_obligatorio(self):
        for record in self:
            if not (record.sNum_registro or '').strip():
                raise ValidationError('El campo «Número de registro» es obligatorio.')

    @api.constrains('iPlazas')
    def _check_iPlazas(self):
        for record in self:
            if record.iPlazas <= 0:
                raise ValidationError('«iPlazas» debe ser mayor que 0.')

    @api.constrains('sNum_registro')
    def _check_sNum_registro_formato(self):
        for record in self:
            if not re.fullmatch(r'[A-Za-z0-9]+([-/._][A-Za-z0-9]+)*', record.sNum_registro or ''):
                raise ValidationError('«Número de registro» solo admite letras y números, separados por - / . _ y sin espacios.')

    @api.constrains('sNum_registro', 'sModelo')
    def _check_longitud(self):
        for record in self:
            for campo in ('sNum_registro', 'sModelo'):
                if record[campo] and len(record[campo]) > 100:
                    raise ValidationError(
                        '«%s» no puede superar los 100 caracteres.' % record._fields[campo].string)

    @api.constrains('sModelo')
    def _check_textos_opcionales(self):
        for record in self:
            for campo in ('sModelo',):
                if record[campo] and not record[campo].strip():
                    raise ValidationError(
                        '«%s» no puede contener solo espacios.' % record._fields[campo].string)
