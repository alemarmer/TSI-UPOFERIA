from odoo import models, fields, api


class MisionDescubrimiento(models.Model):

    _name = 'upoferia.mision_descubrimiento'
    _description = 'Misión de descubrimiento'
    _inherits = {'upoferia.mision': 'mision_id'}
    _rec_name = 'titulo'

    mision_id = fields.Many2one('upoferia.mision', string="Misión", required=True, ondelete='cascade')
    tipo_busqueda = fields.Selection([('objeto', 'Objeto'), ('lugar', 'Lugar'), ('persona', 'Persona')],
                                     string="Tipo de búsqueda")
    arsenal = fields.Text(string="Arsenal", help="Pistas o material disponible para la búsqueda")

    _sql_constraints = [
        ('mision_id_uniq', 'UNIQUE(mision_id)', 'Esa misión ya tiene datos de descubrimiento.'),
    ]

    @api.constrains('mision_id')
    def _check_tipo_unico(self):
        self.mision_id._check_subtipo_unico()

    @api.constrains('tipo_busqueda', 'arsenal')
    def _check_datos_minimos(self):
        for record in self:
            if not record.tipo_busqueda and not (record.arsenal or '').strip():
                raise models.ValidationError('Indica el tipo de búsqueda o el arsenal de la misión.')

    def action_completar(self):
        return self.mision_id.action_completar()