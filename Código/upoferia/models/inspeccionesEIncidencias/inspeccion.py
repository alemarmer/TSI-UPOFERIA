# -*- coding: utf-8 -*-

import re
from datetime import date

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Inspeccion(models.Model):
    _name = 'feria.inspeccion'
    _description = 'Inspección'
    _rec_name = 'sReferencia'
    _sql_constraints = [
        ('referencia_uniq', 'UNIQUE ("sReferencia")',
         'Ya existe una inspección con esa referencia.'),
    ]

    sReferencia = fields.Char(string='Referencia', required=True)
    sTipo = fields.Selection([
        ('seguridad', 'Seguridad e incendios'),
        ('electrica', 'Instalación eléctrica'),
        ('estructural', 'Estructura y montaje'),
        ('sanitaria', 'Sanitaria'),
        ('aforo', 'Aforo'),
        ('veterinaria', 'Veterinaria'),
    ], string='Tipo', required=True)
    sOrganismo = fields.Char(string='Organismo')
    dFecha = fields.Date(string='Fecha', required=True)
    sResultado = fields.Selection([
        ('favorable', 'Favorable'),
        ('favorable_condiciones', 'Favorable con condiciones'),
        ('desfavorable', 'Desfavorable'),
    ], string='Resultado')
    
    sDocumento = fields.Char(string='Documento')
    sEstado = fields.Selection([
        ('programada', 'Programada'),
        ('realizada', 'Realizada'),
        ('cancelada', 'Cancelada'),
    ], string='Estado', required=True, default='programada')

    caseta_id = fields.Many2one('feria.caseta', string='Caseta', required=True, ondelete='restrict')
    punto_control_ids = fields.One2many('feria.punto_control', 'inspeccion_id', string='Puntos de control')
    inspeccion_inspector_ids = fields.One2many('feria.inspeccion_inspector', 'inspeccion_id', string='Inspectores')

    fPorcentajeSuperado = fields.Float(string='Porcentaje superado (%)', compute='_compute_porcentaje_superado', store=True)

    @api.depends('punto_control_ids', 'punto_control_ids.sResultado')
    def _compute_porcentaje_superado(self):
        oRegistro = None
        iTotal = 0
        iSuperados = 0
        for oRegistro in self:
            iTotal = len(oRegistro.punto_control_ids)
            iSuperados = len(oRegistro.punto_control_ids.filtered(lambda oPunto: oPunto.sResultado == 'superado'))
            oRegistro.fPorcentajeSuperado = round(iSuperados / iTotal * 100, 2) if iTotal else 0.0

    @api.constrains('sReferencia')
    def _check_referencia(self):
        oRegistro = None
        sReferencia = ''
        for oRegistro in self:
            sReferencia = oRegistro.sReferencia or ''
            if not sReferencia.strip():
                raise ValidationError('El campo «Referencia» es obligatorio.')
            if not 2 <= len(sReferencia) <= 20:
                raise ValidationError('La «Referencia» de la inspección debe tener entre 2 y 20 caracteres.')
            if not re.fullmatch(r'[A-Z0-9]+([-/._][A-Z0-9]+)*', sReferencia):
                raise ValidationError('La «Referencia» de la inspección solo puede tener letras mayúsculas y números, separados por - / . _ y sin espacios (por ejemplo INS-2026-001).')

    @api.constrains('sOrganismo')
    def _check_organismo(self):
        oRegistro = None
        sOrganismo = ''
        for oRegistro in self:
            sOrganismo = oRegistro.sOrganismo or ''
            if not sOrganismo:
                continue
            if not sOrganismo.strip():
                raise ValidationError('El campo «Organismo» no puede estar formado solo por espacios.')
            if sOrganismo != sOrganismo.strip():
                raise ValidationError('El «Organismo» no puede empezar ni terminar con espacios.')
            if not 2 <= len(sOrganismo) <= 100:
                raise ValidationError('El «Organismo» debe tener entre 2 y 100 caracteres.')

    @api.constrains('dFecha', 'sEstado')
    def _check_fecha(self):
        oRegistro = None
        dHoy = None
        for oRegistro in self:
            dHoy = fields.Date.context_today(oRegistro)
            if not date(1970, 1, 1) <= oRegistro.dFecha <= dHoy + relativedelta(years=1):
                raise ValidationError('La «Fecha» de la inspección debe estar entre el 01/01/1970 y un año después de hoy.')
            if oRegistro.sEstado == 'realizada' and oRegistro.dFecha > dHoy:
                raise ValidationError('Una inspección realizada no puede tener una «Fecha» posterior a hoy.')

    @api.constrains('sEstado', 'sResultado')
    def _check_estado(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.sEstado == 'realizada' and not oRegistro.sResultado:
                raise ValidationError('Una inspección realizada tiene que tener «Resultado».')
            if oRegistro.sEstado != 'realizada' and oRegistro.sResultado:
                raise ValidationError('Solo una inspección realizada puede tener «Resultado».')
            if oRegistro.sEstado != 'realizada' and oRegistro.punto_control_ids.filtered('sResultado'):
                raise ValidationError('La inspección tiene puntos de control con resultado: tiene que estar realizada.')

    @api.constrains('sDocumento')
    def _check_documento(self):
        oRegistro = None
        sDocumento = ''
        for oRegistro in self:
            sDocumento = oRegistro.sDocumento or ''
            if not sDocumento:
                continue
            if re.search(r'\s', sDocumento):
                raise ValidationError('El «Documento» no puede tener espacios.')
            if len(sDocumento) > 255:
                raise ValidationError('El «Documento» puede tener como mucho 255 caracteres.')
            if not re.fullmatch(r'(https?://\S+|\S+\.(pdf|doc|docx|odt))', sDocumento, re.IGNORECASE):
                raise ValidationError('El «Documento» tiene que ser una URL que empiece por http:// o https://, o un archivo .pdf, .doc, .docx u .odt.')
