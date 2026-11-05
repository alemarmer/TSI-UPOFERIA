class ArtistaDisciplina(models.Model):
    _name = 'feria.artista_disciplina'
    _description = 'Disciplina de artista'

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
