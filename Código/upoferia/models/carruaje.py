from odoo import models,fields,api
from odoo.exceptions import ValidationError

class Carruaje(models.Model):
    _name = 'upoferia.carruaje'
    _description = 'Upoferia.carruaje'

    sNum_registro = fields.Char(string='Número de registro', required=True)
    sModelo = fields.Char(string='Modelo')
    iPlazas = fields.Integer(string='Plazas')

    @api.constrains('num_registro')
    def _check_num_registro_obligatorio(self):
        for record in self:
            if not (record.num_registro or '').strip():
                raise ValidationError('El campo «Número de registro» es obligatorio.')

    @api.constrains('plazas')
    def _check_plazas(self):
        for record in self:
            if record.plazas <= 0:
                raise ValidationError('«Plazas» debe ser mayor que 0.')

    @api.constrains('num_registro')
    def _check_num_registro_formato(self):
        for record in self:
            if not re.fullmatch(r'[A-Za-z0-9]+([-/._][A-Za-z0-9]+)*', record.num_registro or ''):
                raise ValidationError('«Número de registro» solo admite letras y números, separados por - / . _ y sin espacios.')

    @api.constrains('num_registro', 'modelo')
    def _check_longitud(self):
        for record in self:
            for campo in ('num_registro', 'modelo'):
                if record[campo] and len(record[campo]) > 100:
                    raise ValidationError(
                        '«%s» no puede superar los 100 caracteres.' % record._fields[campo].string)

    @api.constrains('modelo')
    def _check_textos_opcionales(self):
        for record in self:
            for campo in ('modelo',):
                if record[campo] and not record[campo].strip():
                    raise ValidationError(
                        '«%s» no puede contener solo espacios.' % record._fields[campo].string)
