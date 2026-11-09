# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ParticipacionConcurso(models.Model):
    _name = 'upoferia.participacion_concurso'
    _description = 'Participación en concurso'

    fecha = fields.Date(string='Fecha de inscripción')

    concurso_id = fields.Many2one('upoferia.concurso', string='Concurso', required=True)

    socio_id = fields.Many2one('upoferia.socio', string='Socio', required=True)

    _sql_constraints = [('participacion_socio_concurso_unique', 'UNIQUE ("socio_id", "concurso_id")', 'Ese socio ya está inscrito en ese concurso.')]
