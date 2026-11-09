# -*- coding: utf-8 -*-


import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class Caseta(models.Model):
    _name = 'upoferia.caseta'
    _description = 'Caseta'
    _rec_name = 'sNombre'

    sNombre = fields.Char(string='Nombre', required=True)
    sCalle = fields.Char(string='Calle')
    sNumero = fields.Char(string='Número')
    iModulos = fields.Integer(string='Módulos', required=True, default=1)
    iAforoAutorizado = fields.Integer(string='Aforo autorizado', required=True)
    fHoraApertura = fields.Float(string='Hora de apertura')
    fHoraCierre = fields.Float(string='Hora de cierre')

    _sql_constraints = [
            ('nombre_uniq', 'UNIQUE ("sNombre")',
             'Ya existe una caseta con ese nombre.'),
            ('direccion_uniq', 'UNIQUE ("sCalle", "sNumero")',
             'Ya existe una caseta en esa calle y número.'),
        ]

    zona_ids = fields.One2many('upoferia.zona_caseta', 'caseta_id', string='Zonas')
    mobiliario_ids = fields.One2many('upoferia.mobiliario_caseta', 'caseta_id', string='Mobiliario')
    licencia_ids = fields.One2many('upoferia.licencia', 'caseta_id', string='Licencias')
    inspeccion_ids = fields.One2many('upoferia.inspeccion', 'caseta_id', string='Inspecciones')

    @api.constrains('sNombre')
    def _check_nombre(self):
        oRegistro = None
        sNombre = ''
        for oRegistro in self:
            sNombre = oRegistro.sNombre or ''
            if not sNombre.strip():
                raise ValidationError('El campo «Nombre» es obligatorio.')
            if sNombre != sNombre.strip():
                raise ValidationError('El nombre de la caseta no puede empezar ni terminar con espacios.')
            if not 2 <= len(sNombre) <= 100:
                raise ValidationError('El nombre de la caseta debe tener entre 2 y 100 caracteres.')

    @api.constrains('sCalle')
    def _check_calle(self):
        oRegistro = None
        sCalle = ''
        for oRegistro in self:
            sCalle = oRegistro.sCalle or ''
            if not sCalle:
                continue
            if not sCalle.strip():
                raise ValidationError('El campo «Calle» no puede estar formado solo por espacios.')
            if sCalle != sCalle.strip():
                raise ValidationError('La «Calle» no puede empezar ni terminar con espacios.')
            if not 2 <= len(sCalle) <= 100:
                raise ValidationError('La «Calle» debe tener entre 2 y 100 caracteres.')

    @api.constrains('sNumero', 'sCalle')
    def _check_numero(self):
        oRegistro = None
        sNumero = ''
        for oRegistro in self:
            sNumero = oRegistro.sNumero or ''
            if not sNumero:
                continue
            if not oRegistro.sCalle:
                raise ValidationError('No se puede indicar el «Número» sin indicar la «Calle».')
            if len(sNumero) > 10:
                raise ValidationError('El «Número» de la caseta puede tener como mucho 10 caracteres.')
            if not re.fullmatch(r'[0-9]{1,4}[A-Z]?(-[0-9]{1,4}[A-Z]?)?', sNumero):
                raise ValidationError('El «Número» de la caseta solo puede ser un número, con una letra mayúscula opcional, o un rango de números separados por guion y sin espacios (por ejemplo 12, 12B o 45-47).')

    @api.constrains('iModulos')
    def _check_modulos(self):
        oRegistro = None
        for oRegistro in self:
            if not 1 <= oRegistro.iModulos <= 20:
                raise ValidationError('El número de «Módulos» de la caseta debe estar entre 1 y 20.')

    @api.constrains('iAforoAutorizado')
    def _check_aforo_autorizado(self):
        oRegistro = None
        for oRegistro in self:
            if not 1 <= oRegistro.iAforoAutorizado <= 5000:
                raise ValidationError('El «Aforo autorizado» de la caseta debe estar entre 1 y 5.000 personas.')

    @api.constrains('fHoraApertura')
    def _check_hora_apertura(self):
        oRegistro = None
        for oRegistro in self:
            if not 0 <= oRegistro.fHoraApertura < 24:
                raise ValidationError('La «Hora de apertura» debe estar entre las 00:00 y las 23:59.')

    @api.constrains('fHoraCierre')
    def _check_hora_cierre(self):
        oRegistro = None
        for oRegistro in self:
            if not 0 <= oRegistro.fHoraCierre < 24:
                raise ValidationError('La «Hora de cierre» debe estar entre las 00:00 y las 23:59.')
