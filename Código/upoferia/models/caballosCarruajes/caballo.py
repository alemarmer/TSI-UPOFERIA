# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Caballo(models.Model):
    _name = 'upoferia.caballo'
    _description = 'Caballo'
    _rec_name = 'sMicrochip'

    sMicrochip = fields.Char(string="Microchip del caballo", required=True)
    sNombre = fields.Char(string="Nombre del caballo")
    sRaza = fields.Char(string="Raza del caballo")
    sSexo = fields.Selection([('macho', 'Macho'),
                              ('hembra', 'Hembra'),
                              ('castrado', 'Castrado')],
                             'Sexo')

    salida_ids = fields.Many2many('upoferia.salida', 'upoferia_salida_caballo',
                                  'caballo_id', 'salida_id', string='Salidas')

    #conexion con inspeccion

    _sql_constraints = [('caballo_sMicrochip_unique', 'UNIQUE ("sMicrochip")', 'Ya existe un caballo con ese microchip.')]

    @api.constrains('sMicrochip')
    def _check_sMicrochip(self):
        for record in self:
            if len(record.sMicrochip) != 15 or not record.sMicrochip.isdigit():
                raise models.ValidationError('El microchip debe tener 15 dígitos.')

    @api.constrains('sNombre', 'sRaza')
    def _check_textos(self):
        for record in self:
            if record.sNombre and not record.sNombre.strip():
                raise models.ValidationError('El nombre no puede contener solo espacios.')
            if record.sRaza and not record.sRaza.strip():
                raise models.ValidationError('La raza no puede contener solo espacios.')

    @api.constrains('sNombre', 'sRaza')
    def _check_longitud(self):
        for record in self:
            if record.sNombre and len(record.sNombre) > 100:
                raise models.ValidationError('El nombre no puede superar los 100 caracteres.')
            if record.sRaza and len(record.sRaza) > 100:
                raise models.ValidationError('La raza no puede superar los 100 caracteres.')

    @api.onchange('sMicrochip')
    def onchange_sMicrochip(self):
        resultado = {}
        if self.sMicrochip and (len(self.sMicrochip) != 15 or not self.sMicrochip.isdigit()):
            resultado = {
                'warning': {
                    'title': 'Valores incorrectos',
                    'message': 'El microchip debe tener 15 dígitos.'
                }
            }
        return resultado
