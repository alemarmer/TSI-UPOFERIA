# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Concurso(models.Model):
    _name = 'upoferia.concurso'
    _description = 'Concurso'
    _inherits = {'upoferia.evento': 'evento_id'}
    _rec_name = 'sNombre_evento'

    sBases = fields.Text(string='Bases')
    dFecha_resultado = fields.Date(string='Fecha del resultado')
    sEstado = fields.Selection([('abierto', 'Inscripción abierta'),
                                ('cerrado', 'Inscripción cerrada'),
                                ('resuelto', 'Resuelto')],
                               'Estado', default='abierto')

    evento_id = fields.Many2one('upoferia.evento', string='Evento', required=True)
    jurado_ids = fields.One2many('upoferia.jurado', 'concurso_id', string='Jurado')
    participacion_ids = fields.One2many('upoferia.participacion_concurso', 'concurso_id', string='Participantes')
    premio_ids = fields.One2many('upoferia.premio', 'concurso_id', string='Premios')

    iNum_participantes = fields.Integer(compute='_numParticipantes', string='Número de participantes', store=True)

    _sql_constraints = [('concurso_evento_unique', 'UNIQUE ("evento_id")', 'Ese evento ya está registrado como concurso.')]

    def btn_submit_to_abierto(self):
        self.write({'sEstado': 'abierto'})

    def btn_submit_to_cerrado(self):
        self.write({'sEstado': 'cerrado'})

    def btn_submit_to_resuelto(self):
        self.write({'sEstado': 'resuelto'})

    @api.depends('participacion_ids')
    def _numParticipantes(self):
        for record in self:
            record.iNum_participantes = len(record.participacion_ids)

    @api.constrains('dFecha_resultado', 'dFecha_hora_inicio')
    def _check_dFecha_resultado(self):
        for record in self:
            if record.dFecha_resultado and record.dFecha_hora_inicio and record.dFecha_resultado < record.dFecha_hora_inicio.date():
                raise models.ValidationError('El resultado no puede ser anterior al inicio del concurso.')

    @api.constrains('sBases')
    def _check_sBases(self):
        for record in self:
            if record.sBases and not record.sBases.strip():
                raise models.ValidationError('Las bases no pueden contener solo espacios.')

    @api.onchange('dFecha_resultado', 'dFecha_hora_inicio')
    def onchange_dFecha_resultado(self):
        resultado = {}
        if self.dFecha_resultado and self.dFecha_hora_inicio and self.dFecha_resultado < self.dFecha_hora_inicio.date():
            resultado = {
                'warning': {
                    'title': 'Valores incorrectos',
                    'message': 'El resultado no puede ser anterior al inicio del concurso.'
                }
            }
        return resultado

    @api.onchange('premio_ids')
    def onchange_premio_ids(self):
        resultado = {}
        puestos = self.premio_ids.mapped('iPuesto')
        if len(puestos) != len(set(puestos)):
            resultado = {
                'warning': {
                    'title': 'Valores incorrectos',
                    'message': 'Hay dos premios con el mismo puesto.'
                }
            }
        return resultado
