# -*- coding: utf-8 -*-

import re
from datetime import date

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MobiliarioCaseta(models.Model):
    _name = 'feria.mobiliario_caseta'
    _description = 'Mobiliario de caseta'
    _rec_name = 'sNumeroSerie'
    _sql_constraints = [
        ('numero_serie_uniq', 'UNIQUE ("sNumeroSerie")',
         'Ya existe un mobiliario con ese número de serie.'),
    ]

    sNumeroSerie = fields.Char(string='Número de serie', required=True)
    sNombre = fields.Char(string='Nombre', required=True)
    dFechaAsignacion = fields.Date(string='Fecha de asignación')
    fCoste = fields.Float(string='Coste')

    caseta_id = fields.Many2one('feria.caseta', string='Caseta', ondelete='set null')

    @api.constrains('sNumeroSerie')
    def _check_numero_serie(self):
        oRegistro = None
        sNumeroSerie = ''
        for oRegistro in self:
            sNumeroSerie = oRegistro.sNumeroSerie or ''
            if not sNumeroSerie.strip():
                raise ValidationError('El campo «Número de serie» es obligatorio.')
            if not 2 <= len(sNumeroSerie) <= 30:
                raise ValidationError('El «Número de serie» debe tener entre 2 y 30 caracteres.')
            if not re.fullmatch(r'[A-Z0-9]+([-/._][A-Z0-9]+)*', sNumeroSerie):
                raise ValidationError('El «Número de serie» solo puede tener letras mayúsculas y números, separados por - / . _ y sin espacios (por ejemplo EXT-2026-0001).')

    @api.constrains('sNombre')
    def _check_nombre(self):
        oRegistro = None
        sNombre = ''
        for oRegistro in self:
            sNombre = oRegistro.sNombre or ''
            if not sNombre.strip():
                raise ValidationError('El campo «Nombre» es obligatorio.')
            if sNombre != sNombre.strip():
                raise ValidationError('El nombre del mobiliario no puede empezar ni terminar con espacios.')
            if not 2 <= len(sNombre) <= 100:
                raise ValidationError('El nombre del mobiliario debe tener entre 2 y 100 caracteres.')

    @api.constrains('dFechaAsignacion', 'caseta_id')
    def _check_fecha_asignacion(self):
        oRegistro = None
        dHoy = None
        for oRegistro in self:
            dHoy = fields.Date.context_today(oRegistro)
            if oRegistro.caseta_id and not oRegistro.dFechaAsignacion:
                raise ValidationError('Si el mobiliario está asignado a una caseta hay que indicar la «Fecha de asignación».')
            if not oRegistro.dFechaAsignacion:
                continue
            if not oRegistro.caseta_id:
                raise ValidationError('No se puede indicar la «Fecha de asignación» si el mobiliario no está asignado a ninguna caseta.')
            if not date(1970, 1, 1) <= oRegistro.dFechaAsignacion <= dHoy:
                raise ValidationError('La «Fecha de asignación» debe estar entre el 01/01/1970 y hoy.')

    @api.constrains('fCoste')
    def _check_coste(self):
        oRegistro = None
        fCoste = 0.0
        for oRegistro in self:
            fCoste = oRegistro.fCoste
            if fCoste < 0:
                raise ValidationError('El «Coste» del mobiliario no puede ser negativo.')
            if fCoste > 1000000:
                raise ValidationError('El «Coste» del mobiliario puede ser como mucho de 1.000.000 €.')
            if round(fCoste, 2) != fCoste:
                raise ValidationError('El «Coste» del mobiliario solo admite dos decimales (céntimos).')
