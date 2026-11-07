# -*- coding: utf-8 -*-

from datetime import date

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CopiaLlave(models.Model):
    _name = 'feria.copia_llave'
    _description = 'Copia de llave'
    _rec_name = 'iNumeroCopia'

    iNumeroCopia = fields.Integer(string='Número de copia', required=True)
    dFechaBaja = fields.Date(string='Fecha de baja')
    sEstado = fields.Selection([
        ('activa', 'Activa'),
        ('devuelta', 'Devuelta'),
        ('perdida', 'Perdida'),
    ], string='Estado', required=True, default='activa')
    dFechaEntrega = fields.Date(string='Fecha de entrega')

    @api.depends('iNumeroCopia')
    def _compute_display_name(self):
        oRegistro = None
        for oRegistro in self:
            oRegistro.display_name = f'Copia {oRegistro.iNumeroCopia}'

    @api.constrains('iNumeroCopia')
    def _check_numero_copia(self):
        oRegistro = None
        for oRegistro in self:
            if not 1 <= oRegistro.iNumeroCopia <= 99:
                raise ValidationError('El «Número de copia» debe estar entre 1 y 99.')

    @api.constrains('dFechaEntrega')
    def _check_fecha_entrega(self):
        oRegistro = None
        dHoy = None
        for oRegistro in self:
            if not oRegistro.dFechaEntrega:
                continue
            dHoy = fields.Date.context_today(oRegistro)
            if not date(1970, 1, 1) <= oRegistro.dFechaEntrega <= dHoy:
                raise ValidationError('La «Fecha de entrega» debe estar entre el 01/01/1970 y hoy.')

    @api.constrains('dFechaBaja', 'dFechaEntrega')
    def _check_fecha_baja(self):
        oRegistro = None
        dHoy = None
        for oRegistro in self:
            if not oRegistro.dFechaBaja:
                continue
            dHoy = fields.Date.context_today(oRegistro)
            if not oRegistro.dFechaEntrega:
                raise ValidationError('No se puede indicar la «Fecha de baja» sin la «Fecha de entrega».')
            if oRegistro.dFechaBaja < oRegistro.dFechaEntrega:
                raise ValidationError('La «Fecha de baja» no puede ser anterior a la «Fecha de entrega».')
            if oRegistro.dFechaBaja > dHoy:
                raise ValidationError('La «Fecha de baja» no puede ser posterior a hoy.')

    @api.constrains('sEstado', 'dFechaBaja')
    def _check_estado(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.sEstado == 'activa' and oRegistro.dFechaBaja:
                raise ValidationError('Una copia activa no puede tener «Fecha de baja».')
            if oRegistro.sEstado in ('devuelta', 'perdida') and not oRegistro.dFechaBaja:
                raise ValidationError('Una copia devuelta o perdida tiene que tener «Fecha de baja».')
