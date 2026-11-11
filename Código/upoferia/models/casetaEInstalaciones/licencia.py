# -*- coding: utf-8 -*-

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

    @api.constrains('dFechaCaducidad', 'dFechaConcesion')
    def _check_fecha_caducidad(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.dFechaCaducidad and oRegistro.dFechaConcesion and oRegistro.dFechaCaducidad < oRegistro.dFechaConcesion:
                raise models.ValidationError('La «Fecha de caducidad» no puede ser anterior a la «Fecha de concesión».')
