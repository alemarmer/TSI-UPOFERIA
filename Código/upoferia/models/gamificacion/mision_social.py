from odoo import models, fields, api


class MisionSocial(models.Model):

    _name = 'upoferia.mision_social'
    _description = 'Misión social'
    _inherits = {'upoferia.mision': 'mision_id'}
    _rec_name = 'titulo'

    mision_id = fields.Many2one('upoferia.mision', string="Misión", required=True, ondelete='cascade')
    tipo_reto = fields.Selection([('invitar', 'Invitar amigos'), ('clan', 'Reunir al clan'),
                                  ('coincidir', 'Coincidir en la caseta')], string="Tipo de reto")
    contador_personas = fields.Integer(string="Personas a reunir", default=2,
                                       help="Número de personas que hay que reunir para completar el reto")

    _sql_constraints = [
        ('mision_id_uniq', 'UNIQUE(mision_id)', 'Esa misión ya tiene datos sociales.'),
        ('contador_positivo', 'CHECK(contador_personas > 0)', 'El número de personas debe ser mayor que 0.'),
    ]

    @api.constrains('mision_id')
    def _check_tipo_unico(self):
        self.mision_id._check_subtipo_unico()

    @api.constrains('tipo_reto', 'mision_id')
    def _check_reto_clan(self):
        for record in self:
            if record.tipo_reto == 'clan' and not record.registro_xp_id.socio_id.clan_id:
                raise models.ValidationError('El socio no pertenece a ningún clan: no puede tener un reto de clan.')

    def action_completar(self):
        return self.mision_id.action_completar()