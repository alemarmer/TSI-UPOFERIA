# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ElementoSeguridad(models.Model):
    _name = 'upoferia.elemento_seguridad'
    _description = 'Elemento de seguridad'
    _inherits = {'upoferia.mobiliario_caseta': 'mobiliario_id'}
    _rec_name = 'sNumeroSerie'

    sTipo = fields.Selection([
        ('extintor', 'Extintor'),
        ('botiquin', 'Botiquín'),
        ('detector_humo', 'Detector de humo'),
        ('luz_emergencia', 'Luz de emergencia'),
        ('senal_evacuacion', 'Señal de evacuación'),
        ('manta_ignifuga', 'Manta ignífuga'),
        ('desfibrilador', 'Desfibrilador'),
    ], string='Tipo', required=True)
    dFechaUltimaRevision = fields.Date(string='Fecha de la última revisión')
    dFechaProximaRevision = fields.Date(string='Fecha de la próxima revisión')

    mobiliario_id = fields.Many2one('upoferia.mobiliario_caseta', string='Mobiliario', required=True)

    bRevisionVencida = fields.Boolean(string='Revisión vencida', compute='_compute_revision_vencida')

    _sql_constraints = [
                    ('mobiliario_uniq', 'UNIQUE (mobiliario_id)',
                     'Ese mobiliario ya está registrado como elemento de seguridad.'),
    ]

    @api.depends('dFechaProximaRevision')
    def _compute_revision_vencida(self):
        oRegistro = None
        dHoy = None
        for oRegistro in self:
            dHoy = fields.Date.context_today(oRegistro)
            oRegistro.bRevisionVencida = bool(oRegistro.dFechaProximaRevision and oRegistro.dFechaProximaRevision < dHoy)

    @api.constrains('dFechaProximaRevision', 'dFechaUltimaRevision')
    def _check_fecha_proxima_revision(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.dFechaProximaRevision and oRegistro.dFechaUltimaRevision and oRegistro.dFechaProximaRevision <= oRegistro.dFechaUltimaRevision:
                raise models.ValidationError('La «Fecha de la próxima revisión» tiene que ser posterior a la de la última revisión.')

    def unlink(self):
        oMobiliarios = self.mobiliario_id
        bResultado = super().unlink()
        oMobiliarios.unlink()
        return bResultado
