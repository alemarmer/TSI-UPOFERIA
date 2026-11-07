from odoo import models,fields,api
from odoo.exceptions import ValidationError
import re

class Caballo(models.Model):

    _name='upoferia.caballo' 
    _description='Upoferia.caballo'
    _rec_name = 'sMicrochip'
    _sql_constraints = [
        ('sMicrochip_uniq', 'UNIQUE ("sMicrochip")',
         'Ya existe un caballo con ese Microchip.'),
    ]

    sMicrochip= fields.Char(string="Microchip del caballo", size=60, required=True) 
    sNombre = fields.Char(string="Nombre del caballo", size=100)
    sRaza = fields.Char(string="Raza del caballo", size=100)
    sSexo = fields.Selection([('macho', 'Macho'),
                             ('hembra', 'Hembra'),
                             ('castrado', 'Castrado')],
                            string='Sexo')

    salida_ids = fields.Many2many('upoferia.salida', 'upoferia_salida_caballo',
                                  'caballo_id', 'salida_id', string='Salidas')

    #conexion con inspeccion

    @api.constrains('sMicrochip')
    def _check_sMicrochip_formato(self):
        for record in self:
            if not re.fullmatch(r'[0-9]{15}', record.sMicrochip or ''):
                raise ValidationError('El sMicrochip debe tener 15 dígitos (norma ISO 11784/11785).')

    @api.constrains('sNombre', 'sRaza')
    def _check_longitud(self):
        for record in self:
            for campo in ('sNombre', 'sRaza'):
                if record[campo] and len(record[campo]) > 100:
                    raise ValidationError(
                        '«%s» no puede superar los 100 caracteres.' % record._fields[campo].string)

    @api.constrains('sNombre', 'sRaza')
    def _check_textos_opcionales(self):
        for record in self:
            for campo in ('sNombre', 'sRaza'):
                if record[campo] and not record[campo].strip():
                    raise ValidationError(
                        '«%s» no puede contener solo espacios.' % record._fields[campo].string)
