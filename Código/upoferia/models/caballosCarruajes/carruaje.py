# -*- coding: utf-8 -*-

from odoo import models,fields,api


class Carruaje(models.Model):
    _name = 'upoferia.carruaje'
    _description = 'Upoferia.carruaje'
    _rec_name = 'sNum_registro'

    sNum_registro = fields.Char(string='Número de registro', required=True)
    sModelo = fields.Char(string='Modelo')
    iPlazas = fields.Integer(string='Plazas')
    salida_ids = fields.One2many('upoferia.salida', 'carruaje_id', string='Salidas')
    licencia_ids = fields.One2many('upoferia.licencia', 'carruaje_id', string='Licencias')

    _sql_constraints = [('carruaje_sNum_registro_unique', 'UNIQUE ("sNum_registro")', 'Ya existe un carruaje con ese número de registro.')]


    @api.constrains('iPlazas')
    def _check_iPlazas(self):
        for record in self:
            if record.iPlazas <= 0:
                raise models.ValidationError('El número de plazas debe ser mayor que 0.')

    @api.constrains('sNum_registro')
    def _check_sNum_registro_formato(self):
        for record in self:
            if not re.fullmatch(r'[A-Za-z0-9]+([-/._][A-Za-z0-9]+)*', record.sNum_registro or ''):
                raise ValidationError('«Número de registro» solo admite letras y números, separados por - / . _ y sin espacios.')

    @api.constrains('sModelo')
    def _check_sModelo(self):
        for record in self:
            if record.sModelo and not record.sModelo.strip():
                raise models.ValidationError('El modelo no puede contener solo espacios.')

    @api.constrains('sNum_registro', 'sModelo')
    def _check_longitud(self):
        for record in self:
            if record.sNum_registro and len(record.sNum_registro) > 100:
                raise models.ValidationError('El número de registro no puede superar los 100 caracteres.')
            if record.sModelo and len(record.sModelo) > 100:
                raise models.ValidationError('El modelo no puede superar los 100 caracteres.')

