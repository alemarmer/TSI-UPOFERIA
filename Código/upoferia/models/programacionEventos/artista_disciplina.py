from odoo import models,fields,api
from odoo.exceptions import ValidationError

class ArtistaDisciplina(models.Model):
    _name = 'upoferia.artista_disciplina'
    _description = 'Upoferia.artista_disciplina'
    _rec_name = 'sDisciplina'

    sDisciplina = fields.Char(string='Disciplina', required=True)

    artista_id = fields.Many2one('upoferia.artista', string='Artista', required=True, ondelete='cascade') 

    @api.constrains('sDisciplina')
    def _check_sDisciplina_obligatorio(self):
        for record in self:
            if not (record.sDisciplina or '').strip():
                raise ValidationError('El campo «Disciplina» es obligatorio.')

    @api.constrains('sDisciplina')
    def _check_longitud(self):
        for record in self:
            for campo in ('sDisciplina',):
                if record[campo] and len(record[campo]) > 100:
                    raise ValidationError(
                        '«%s» no puede superar los 100 caracteres.' % record._fields[campo].string)
