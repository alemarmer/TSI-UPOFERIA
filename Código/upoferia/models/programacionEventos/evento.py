# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta


class Evento(models.Model):
    _name = 'upoferia.evento'
    _description = 'Evento'
    _rec_name = 'sNombre_evento'

    sNombre_evento = fields.Char(string="Nombre del evento", required=True)
    dFecha_hora_inicio = fields.Datetime(string='Fecha y hora de inicio')
    dFecha_hora_fin = fields.Datetime(string='Fecha y hora de finalización')
    iAforo_reservado = fields.Integer(string='Aforo reservado')
    sEstado = fields.Selection([('programado', 'Programado'),
                                ('en_curso', 'En curso'),
                                ('finalizado', 'Finalizado'),
                                ('cancelado', 'Cancelado')],
                               'Estado', default='programado')
    iPlazas_libres = fields.Integer(compute='_plazasLibres', string='Plazas libres', store=True)

    tipo_evento_id = fields.Many2one('upoferia.tipo_evento', string='Tipo de evento', required=True)
    concurso_ids = fields.One2many('upoferia.concurso', 'evento_id', string='Concurso')
    actuacion_ids = fields.One2many('upoferia.actuacion', 'evento_id', string='Actuación')
    patrocinio_ids = fields.One2many('upoferia.patrocinio', 'evento_id', string='Patrocinios')
    fDuracion = fields.Float(compute='_duracionTotal', string='Duración (horas)', store=True)
    caseta_id = fields.Many2one('upoferia.caseta', string='Caseta', required=True)

    _sql_constraints = [('evento_sNombre_evento_unique', 'UNIQUE ("sNombre_evento")', 'Ya existe un evento con ese nombre.')]

    def btn_submit_to_programado(self):
        self.write({'sEstado': 'programado'})

    def btn_submit_to_en_curso(self):
        self.write({'sEstado': 'en_curso'})

    def btn_submit_to_finalizado(self):
        self.write({'sEstado': 'finalizado'})

    def btn_submit_to_cancelado(self):
        self.write({'sEstado': 'cancelado'})

    @api.depends('dFecha_hora_inicio', 'dFecha_hora_fin')
    def _duracionTotal(self):
        for record in self:
            if record.dFecha_hora_inicio and record.dFecha_hora_fin:
                record.fDuracion = (record.dFecha_hora_fin - record.dFecha_hora_inicio).total_seconds() / 3600
            else:
                record.fDuracion = 0

    @api.depends('caseta_id.iAforo_autorizado', 'iAforo_reservado')
    def _plazasLibres(self):
        for record in self:
            record.iPlazas_libres = record.caseta_id.iAforo_autorizado - record.iAforo_reservado

    @api.constrains('sNombre_evento')
    def _check_sNombre_evento(self):
        for record in self:
            if not record.sNombre_evento.strip():
                raise models.ValidationError('El nombre del evento es obligatorio.')

    @api.constrains('sNombre_evento')
    def _check_longitud(self):
        for record in self:
            if record.sNombre_evento and len(record.sNombre_evento) > 100:
                raise models.ValidationError('El nombre del evento no puede superar los 100 caracteres.')

    @api.constrains('dFecha_hora_inicio', 'dFecha_hora_fin')
    def _check_fechas(self):
        for record in self:
            if record.dFecha_hora_fin and not record.dFecha_hora_inicio:
                raise models.ValidationError('Si hay fecha de fin, también tiene que haber fecha de inicio.')
            if record.dFecha_hora_fin and record.dFecha_hora_fin <= record.dFecha_hora_inicio:
                raise models.ValidationError('El fin debe ser posterior al inicio.')

    @api.constrains('iAforo_reservado', 'caseta_id')
    def _check_iAforo_reservado(self):
        for record in self:
            if record.iAforo_reservado < 0:
                raise models.ValidationError('El aforo reservado no puede ser negativo.')
            if record.iAforo_reservado > record.caseta_id.iAforo_autorizado:
                raise models.ValidationError('El aforo reservado no puede superar el aforo autorizado de la caseta.')

    @api.onchange('dFecha_hora_inicio', 'dFecha_hora_fin')
    def onchange_fechas(self):
        resultado = {}
        if self.dFecha_hora_inicio and self.dFecha_hora_fin and self.dFecha_hora_fin <= self.dFecha_hora_inicio:
            resultado = {
                'warning': {
                    'title': 'Valores incorrectos',
                    'message': 'El fin debe ser posterior al inicio.'
                }
            }
        return resultado

    @api.onchange('dFecha_hora_inicio')
    def onchange_dFecha_hora_inicio(self):
        resultado = {}
        if self.dFecha_hora_inicio and not self.dFecha_hora_fin:
            resultado = {
                'value': {'dFecha_hora_fin': self.dFecha_hora_inicio + timedelta(hours=2)}
            }
        return resultado
