# -*- coding: utf-8 -*-

import re
from datetime import date

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Incidencia(models.Model):
    _name = 'upoferia.incidencia'
    _description = 'Incidencia'
    _rec_name = 'sReferencia'
    _sql_constraints = [
        ('referencia_uniq', 'UNIQUE ("sReferencia")',
         'Ya existe una incidencia con esa referencia.'),
    ]

    sReferencia = fields.Char(string='Referencia', required=True)
    dFecha = fields.Date(string='Fecha', required=True, default=fields.Date.context_today)
    sPrioridad = fields.Selection([
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ], string='Prioridad', required=True, default='media')
    sEstado = fields.Selection([
        ('abierta', 'Abierta'),
        ('en_curso', 'En curso'),
        ('resuelta', 'Resuelta'),
        ('cancelada', 'Cancelada'),
    ], string='Estado', required=True, default='abierta')

    mobiliario_id = fields.Many2one('upoferia.mobiliario_caseta', string='Mobiliario afectado')

    punto_control_id = fields.Many2one('upoferia.punto_control', string='Punto de control que la detecta')
    mantenimiento_ids = fields.One2many('upoferia.mantenimiento', 'incidencia_id', string='Mantenimientos')

    @api.constrains('sReferencia')
    def _check_referencia(self):
        oRegistro = None
        sReferencia = ''
        for oRegistro in self:
            sReferencia = oRegistro.sReferencia or ''
            if not sReferencia.strip():
                raise ValidationError('El campo «Referencia» es obligatorio.')
            if not 2 <= len(sReferencia) <= 20:
                raise ValidationError('La «Referencia» de la incidencia debe tener entre 2 y 20 caracteres.')
            if not re.fullmatch(r'[A-Z0-9]+([-/._][A-Z0-9]+)*', sReferencia):
                raise ValidationError('La «Referencia» de la incidencia solo puede tener letras mayúsculas y números, separados por - / . _ y sin espacios (por ejemplo INC-2026-001).')

    @api.constrains('dFecha', 'punto_control_id')
    def _check_fecha(self):
        oRegistro = None
        dHoy = None
        for oRegistro in self:
            dHoy = fields.Date.context_today(oRegistro)
            if not date(1970, 1, 1) <= oRegistro.dFecha <= dHoy:
                raise ValidationError('La «Fecha» de la incidencia debe estar entre el 01/01/1970 y hoy.')
            if oRegistro.punto_control_id and oRegistro.dFecha < oRegistro.punto_control_id.inspeccion_id.dFecha:
                raise ValidationError('La «Fecha» de la incidencia no puede ser anterior a la de la inspección que la detecta.')

    @api.constrains('punto_control_id', 'mobiliario_id')
    def _check_punto_control(self):
        oRegistro = None
        oPunto = None
        for oRegistro in self:
            oPunto = oRegistro.punto_control_id
            if not oPunto:
                continue
            if oPunto.sResultado != 'no_superado':
                raise ValidationError('Una incidencia solo la puede detectar un punto de control no superado.')
            if oRegistro.mobiliario_id and oRegistro.mobiliario_id.caseta_id != oPunto.inspeccion_id.caseta_id:
                raise ValidationError('Si la incidencia la detecta un punto de control, el mobiliario afectado tiene que ser de la caseta inspeccionada.')
