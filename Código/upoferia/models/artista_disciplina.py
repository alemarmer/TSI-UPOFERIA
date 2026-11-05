from odoo import models,fields,api

class ArtistaDisciplina(models.Model):
    _name = 'upoferia.artista_disciplina'
    _description = 'Upoferia.artista_disciplina'

    artista_id = fields.Many2one('upoferia.artista', string='Artista', required=True, ondelete='cascade') 
    disciplina = fields.Char(string='Disciplina', required=True)

    @api.constrains('disciplina')
    def _check_disciplina_obligatorio(self):
        for record in self:
            if not (record.disciplina or '').strip():
                raise ValidationError('El campo «Disciplina» es obligatorio.')

    @api.constrains('disciplina')
    def _check_longitud(self):
        for record in self:
            for campo in ('disciplina',):
                if record[campo] and len(record[campo]) > 100:
                    raise ValidationError(
                        '«%s» no puede superar los 100 caracteres.' % record._fields[campo].string)
