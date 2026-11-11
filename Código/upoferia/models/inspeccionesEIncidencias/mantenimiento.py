# -*- coding: utf-8 -*-

from odoo import models, fields, api


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

    incidencia_id = fields.Many2one('upoferia.incidencia', string='Incidencia')

    @api.constrains('dFechaProgramada', 'dFechaSolicitud')
    def _check_fecha_programada(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.dFechaProgramada and oRegistro.dFechaProgramada < oRegistro.dFechaSolicitud:
                raise models.ValidationError('La «Fecha programada» no puede ser anterior a la «Fecha de solicitud».')

    @api.constrains('sTipoMantenimiento', 'incidencia_id')
    def _check_tipo_mantenimiento(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.sTipoMantenimiento == 'correctivo' and not oRegistro.incidencia_id:
                raise models.ValidationError('Un mantenimiento correctivo tiene que estar asociado a una incidencia.')
