from odoo import models, fields


class Salida(models.Model):
    _inherit = 'upoferia.salida'

    transaccion_id = fields.Many2one('feria.transaccion', string='Transacción', ondelete='set null')
