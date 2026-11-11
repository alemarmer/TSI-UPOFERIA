# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Jurado(models.Model):
    _name = 'upoferia.jurado'
    _description = 'Miembro del jurado'
    _rec_name = 'sRol'

    sRol = fields.Selection([('presidente', 'Presidente'),
                             ('vocal', 'Vocal'),
                             ('secretario', 'Secretario')],
                            'Rol')

    concurso_id = fields.Many2one('upoferia.concurso', string='Concurso', required=True)

    persona_id = fields.Many2one('upoferia.socios.persona', string='Miembro', required=True)

    _sql_constraints = [('jurado_concurso_persona_unique', 'UNIQUE ("concurso_id", "persona_id")', 'Esa persona ya está en el jurado de ese concurso.')]
