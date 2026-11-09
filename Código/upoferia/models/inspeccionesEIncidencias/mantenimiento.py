# -*- coding: utf-8 -*-

import re
from datetime import date

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Mantenimiento(models.Model):
    _name = 'upoferia.mantenimiento'
    _description = 'Mantenimiento'
    _rec_name = 'sIdMantenimiento'
    _sql_constraints = [
        ('id_mantenimiento_uniq', 'UNIQUE ("sIdMantenimiento")',
         'Ya existe un mantenimiento con ese identificador.'),
    ]

    sIdMantenimiento = fields.Char(string='Id. mantenimiento', required=True)
    sAsunto = fields.Char(string='Asunto', required=True)
    sTipoMantenimiento = fields.Selection([
        ('preventivo', 'Preventivo'),
        ('correctivo', 'Correctivo'),
    ], string='Tipo de mantenimiento', required=True)
    dFechaSolicitud = fields.Date(string='Fecha de solicitud', required=True, default=fields.Date.context_today)
    dFechaProgramada = fields.Date(string='Fecha programada')
    fDuracionHoras = fields.Float(string='Duración (horas)')
    sEstado = fields.Selection([
        ('solicitado', 'Solicitado'),
        ('programado', 'Programado'),
        ('en_curso', 'En curso'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ], string='Estado', required=True, default='solicitado')

    incidencia_id = fields.Many2one('upoferia.incidencia', string='Incidencia', ondelete='set null')

    @api.constrains('sIdMantenimiento')
    def _check_id_mantenimiento(self):
        oRegistro = None
        sIdMantenimiento = ''
        for oRegistro in self:
            sIdMantenimiento = oRegistro.sIdMantenimiento or ''
            if not sIdMantenimiento.strip():
                raise ValidationError('El campo «Id. mantenimiento» es obligatorio.')
            if not 2 <= len(sIdMantenimiento) <= 20:
                raise ValidationError('El «Id. mantenimiento» debe tener entre 2 y 20 caracteres.')
            if not re.fullmatch(r'[A-Z0-9]+([-/._][A-Z0-9]+)*', sIdMantenimiento):
                raise ValidationError('El «Id. mantenimiento» solo puede tener letras mayúsculas y números, separados por - / . _ y sin espacios (por ejemplo MNT-2026-001).')

    @api.constrains('sAsunto')
    def _check_asunto(self):
        oRegistro = None
        sAsunto = ''
        for oRegistro in self:
            sAsunto = oRegistro.sAsunto or ''
            if not sAsunto.strip():
                raise ValidationError('El campo «Asunto» es obligatorio.')
            if sAsunto != sAsunto.strip():
                raise ValidationError('El «Asunto» del mantenimiento no puede empezar ni terminar con espacios.')
            if not 2 <= len(sAsunto) <= 100:
                raise ValidationError('El «Asunto» del mantenimiento debe tener entre 2 y 100 caracteres.')

    @api.constrains('dFechaSolicitud', 'incidencia_id')
    def _check_fecha_solicitud(self):
        oRegistro = None
        dHoy = None
        for oRegistro in self:
            dHoy = fields.Date.context_today(oRegistro)
            if not date(1970, 1, 1) <= oRegistro.dFechaSolicitud <= dHoy:
                raise ValidationError('La «Fecha de solicitud» debe estar entre el 01/01/1970 y hoy.')
            if oRegistro.incidencia_id and oRegistro.dFechaSolicitud < oRegistro.incidencia_id.dFecha:
                raise ValidationError('La «Fecha de solicitud» no puede ser anterior a la fecha de la incidencia.')

    @api.constrains('dFechaProgramada', 'dFechaSolicitud')
    def _check_fecha_programada(self):
        oRegistro = None
        for oRegistro in self:
            if not oRegistro.dFechaProgramada:
                continue
            if oRegistro.dFechaProgramada < oRegistro.dFechaSolicitud:
                raise ValidationError('La «Fecha programada» no puede ser anterior a la «Fecha de solicitud».')
            if oRegistro.dFechaProgramada > oRegistro.dFechaSolicitud + relativedelta(years=1):
                raise ValidationError('La «Fecha programada» puede ser como mucho un año después de la «Fecha de solicitud».')

    @api.constrains('fDuracionHoras')
    def _check_duracion_horas(self):
        oRegistro = None
        fDuracion = 0.0
        for oRegistro in self:
            fDuracion = oRegistro.fDuracionHoras
            if fDuracion < 0:
                raise ValidationError('La «Duración» del mantenimiento no puede ser negativa.')
            if fDuracion > 500:
                raise ValidationError('La «Duración» del mantenimiento puede ser como mucho de 500 horas.')
            if round(fDuracion, 2) != fDuracion:
                raise ValidationError('La «Duración» del mantenimiento solo admite dos decimales.')

    @api.constrains('sEstado', 'dFechaProgramada', 'fDuracionHoras')
    def _check_estado(self):
        oRegistro = None
        dHoy = None
        for oRegistro in self:
            dHoy = fields.Date.context_today(oRegistro)
            if oRegistro.sEstado in ('programado', 'en_curso', 'finalizado') and not oRegistro.dFechaProgramada:
                raise ValidationError('Un mantenimiento programado, en curso o finalizado tiene que tener «Fecha programada».')
            if oRegistro.sEstado in ('en_curso', 'finalizado') and oRegistro.dFechaProgramada > dHoy:
                raise ValidationError('Un mantenimiento en curso o finalizado no puede tener una «Fecha programada» posterior a hoy.')
            if oRegistro.sEstado == 'finalizado' and oRegistro.fDuracionHoras <= 0:
                raise ValidationError('Un mantenimiento finalizado tiene que tener una «Duración» mayor que 0.')

    @api.constrains('sTipoMantenimiento', 'incidencia_id')
    def _check_tipo_mantenimiento(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.sTipoMantenimiento == 'correctivo' and not oRegistro.incidencia_id:
                raise ValidationError('Un mantenimiento correctivo tiene que estar asociado a una incidencia.')
            if oRegistro.sTipoMantenimiento == 'preventivo' and oRegistro.incidencia_id:
                raise ValidationError('Un mantenimiento preventivo no puede estar asociado a una incidencia.')
