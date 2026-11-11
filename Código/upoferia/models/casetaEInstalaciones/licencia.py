# -*- coding: utf-8 -*-

import re
from datetime import date

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api


class Licencia(models.Model):
    _name = 'upoferia.licencia'
    _description = 'Licencia'
    _rec_name = 'sNumeroExpediente'
    _sql_constraints = [
        ('numero_expediente_uniq', 'UNIQUE ("sNumeroExpediente")',
         'Ya existe una licencia con ese número de expediente.'),
    ]

    sNumeroExpediente = fields.Char(string='Número de expediente', required=True)
    sTipo = fields.Selection([
        ('apertura', 'Apertura de caseta'),
        ('actividad', 'Actividad'),
        ('montaje', 'Montaje e instalación'),
        ('musica', 'Música y ambientación'),
        ('sanitaria', 'Sanitaria'),
        ('carruaje', 'Circulación de carruaje'),
    ], string='Tipo', required=True)
    sOrganismo = fields.Char(string='Organismo')
    dFechaConcesion = fields.Date(string='Fecha de concesión')
    dFechaCaducidad = fields.Date(string='Fecha de caducidad')
    sEstado = fields.Selection([
        ('solicitada', 'Solicitada'),
        ('concedida', 'Concedida'),
        ('denegada', 'Denegada'),
        ('revocada', 'Revocada'),
    ], string='Estado', required=True, default='solicitada')

    sDocumento = fields.Char(string='Documento')

    caseta_id = fields.Many2one('upoferia.caseta', string='Caseta', required=True)

    bVigente = fields.Boolean(string='Vigente', compute='_compute_vigente')

    @api.depends('sEstado', 'dFechaConcesion', 'dFechaCaducidad')
    def _compute_vigente(self):
        oRegistro = None
        dHoy = None
        for oRegistro in self:
            dHoy = fields.Date.context_today(oRegistro)
            oRegistro.bVigente = bool(
                oRegistro.sEstado == 'concedida'
                and oRegistro.dFechaConcesion
                and oRegistro.dFechaCaducidad
                and oRegistro.dFechaConcesion <= dHoy <= oRegistro.dFechaCaducidad
            )

    @api.constrains('sNumeroExpediente')
    def _check_numero_expediente(self):
        oRegistro = None
        sNumeroExpediente = ''
        for oRegistro in self:
            sNumeroExpediente = oRegistro.sNumeroExpediente or ''
            if not sNumeroExpediente.strip():
                raise models.ValidationError('El campo «Número de expediente» es obligatorio.')
            if not 2 <= len(sNumeroExpediente) <= 20:
                raise models.ValidationError('El «Número de expediente» debe tener entre 2 y 20 caracteres.')
            if not re.fullmatch(r'[A-Z0-9]+([-/._][A-Z0-9]+)*', sNumeroExpediente):
                raise models.ValidationError('El «Número de expediente» solo puede tener letras mayúsculas y números, separados por - / . _ y sin espacios (por ejemplo EXP-2026/0001).')

    @api.constrains('sOrganismo')
    def _check_organismo(self):
        oRegistro = None
        sOrganismo = ''
        for oRegistro in self:
            sOrganismo = oRegistro.sOrganismo or ''
            if not sOrganismo:
                continue
            if not sOrganismo.strip():
                raise models.ValidationError('El campo «Organismo» no puede estar formado solo por espacios.')
            if sOrganismo != sOrganismo.strip():
                raise models.ValidationError('El «Organismo» no puede empezar ni terminar con espacios.')
            if not 2 <= len(sOrganismo) <= 100:
                raise models.ValidationError('El «Organismo» debe tener entre 2 y 100 caracteres.')

    @api.constrains('dFechaConcesion')
    def _check_fecha_concesion(self):
        oRegistro = None
        dHoy = None
        for oRegistro in self:
            if not oRegistro.dFechaConcesion:
                continue
            dHoy = fields.Date.context_today(oRegistro)
            if not date(1970, 1, 1) <= oRegistro.dFechaConcesion <= dHoy:
                raise models.ValidationError('La «Fecha de concesión» debe estar entre el 01/01/1970 y hoy.')

    @api.constrains('dFechaCaducidad', 'dFechaConcesion')
    def _check_fecha_caducidad(self):
        oRegistro = None
        for oRegistro in self:
            if not oRegistro.dFechaCaducidad:
                continue
            if not oRegistro.dFechaConcesion:
                raise models.ValidationError('No se puede indicar la «Fecha de caducidad» sin la «Fecha de concesión».')
            if oRegistro.dFechaCaducidad < oRegistro.dFechaConcesion:
                raise models.ValidationError('La «Fecha de caducidad» no puede ser anterior a la «Fecha de concesión».')
            if oRegistro.dFechaCaducidad > oRegistro.dFechaConcesion + relativedelta(years=10):
                raise models.ValidationError('La «Fecha de caducidad» puede ser como mucho diez años después de la «Fecha de concesión».')

    @api.constrains('sEstado', 'dFechaConcesion', 'dFechaCaducidad')
    def _check_estado(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.sEstado in ('concedida', 'revocada'):
                if not oRegistro.dFechaConcesion or not oRegistro.dFechaCaducidad:
                    raise models.ValidationError('Una licencia concedida o revocada tiene que tener «Fecha de concesión» y «Fecha de caducidad».')
            elif oRegistro.dFechaConcesion or oRegistro.dFechaCaducidad:
                raise models.ValidationError('Una licencia solicitada o denegada no puede tener «Fecha de concesión» ni «Fecha de caducidad».')

    @api.constrains('sDocumento')
    def _check_documento(self):
        oRegistro = None
        sDocumento = ''
        for oRegistro in self:
            sDocumento = oRegistro.sDocumento or ''
            if not sDocumento:
                continue
            if re.search(r'\s', sDocumento):
                raise models.ValidationError('El «Documento» no puede tener espacios.')
            if len(sDocumento) > 255:
                raise models.ValidationError('El «Documento» puede tener como mucho 255 caracteres.')
            if not re.fullmatch(r'(https?://\S+|\S+\.(pdf|doc|docx|odt))', sDocumento, re.IGNORECASE):
                raise models.ValidationError('El «Documento» tiene que ser una URL que empiece por http:// o https://, o un archivo .pdf, .doc, .docx u .odt.')
