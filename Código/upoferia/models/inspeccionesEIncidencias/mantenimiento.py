# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Mantenimiento(models.Model):
    _name = 'upoferia.mantenimiento'
    _description = 'Mantenimiento'
    _rec_name = 'sIdMantenimiento'

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
    transaccion_id = fields.Many2one('upoferia.transaccion', string='Contrato')
    tecnico_ids = fields.Many2many('upoferia.tecnico', 'upoferia_mantenimiento_tecnico_rel', 'mantenimiento_id', 'tecnico_id', string='Técnicos')

    _sql_constraints = [
            ('id_mantenimiento_uniq', 'UNIQUE ("sIdMantenimiento")',
             'Ya existe un mantenimiento con ese identificador.'),
    ]

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

    @api.constrains('transaccion_id')
    def _check_transaccion(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.transaccion_id and oRegistro.transaccion_id.tipo_transaccion_id.sCodigo != 'CON':
                raise models.ValidationError('El mantenimiento solo puede estar cubierto por un contrato (transacción de tipo CON).')