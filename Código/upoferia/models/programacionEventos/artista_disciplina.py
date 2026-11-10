# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ArtistaDisciplina(models.Model):
    _name = 'upoferia.artista_disciplina'
    _description = 'Disciplina de artista'
    _rec_name = 'sDisciplina'

    sDisciplina = fields.Char(string='Disciplina', required=True)

    artista_id = fields.Many2one('upoferia.artista', string='Artista', required=True) 

    _sql_constraints = [('artista_disciplina_unique', 'UNIQUE ("artista_id", "sDisciplina")', 'Ese artista ya tiene esa disciplina.')]


    @api.constrains('sDisciplina')
    def _check_sDisciplina(self):
        for record in self:
            if not record.sDisciplina.strip():
                raise models.ValidationError('La disciplina es obligatoria.')

    @api.constrains('sDisciplina')
    def _check_longitud(self):
        for record in self:
            if record.sDisciplina and len(record.sDisciplina) > 100:
                raise models.ValidationError('La disciplina no puede superar los 100 caracteres.')
