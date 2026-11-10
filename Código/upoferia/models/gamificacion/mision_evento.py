from odoo import models, fields, api


class MisionEvento(models.Model):

    _name = 'upoferia.mision_evento'
    _description = 'Misión de evento'
    _inherits = {'upoferia.mision': 'mision_id'}
    _rec_name = 'titulo'

    mision_id = fields.Many2one('upoferia.mision', string="Misión", required=True, ondelete='cascade')
    tipo_evento = fields.Selection([('actuacion', 'Actuación'), ('concurso', 'Concurso'),
                                    ('fiesta', 'Fiesta'), ('otro', 'Otro')], string="Tipo de evento")
    fecha = fields.Date(string="Fecha del evento")

    _sql_constraints = [
        ('mision_id_uniq', 'UNIQUE(mision_id)', 'Esa misión ya tiene datos de evento.'),
    ]

    @api.constrains('mision_id')
    def _check_tipo_unico(self):
        self.mision_id._check_subtipo_unico()

    @api.constrains('fecha', 'mision_id')
    def _check_fecha_en_temporada(self):
        for record in self:
            temporada = record.registro_xp_id.temporada_pase_id
            if record.fecha and not (temporada.fecha_inicio <= record.fecha <= temporada.fecha_fin):
                raise models.ValidationError('La fecha del evento debe estar dentro de la temporada «%s».' % temporada.nombre)

    @api.onchange('fecha')
    def onchange_fecha(self):
        if self.fecha and not self.fecha_max:
            self.fecha_max = self.fecha

    def action_completar(self):
        return self.mision_id.action_completar()