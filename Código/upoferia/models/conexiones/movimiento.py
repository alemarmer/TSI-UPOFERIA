from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Movimiento(models.Model):
    _inherit = 'upoferia.movimiento'

    transaccion_id = fields.Many2one('feria.transaccion', string='Transacción', ondelete='restrict')

    @api.constrains('transaccion_id')
    def _check_transaccion(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.transaccion_id and oRegistro.transaccion_id.tipo_transaccion_id.sCodigo not in ('FAC', 'ABO'):
                raise ValidationError('Un movimiento solo se puede asociar a una FAC o un ABO (%s es %s).' % (
                    oRegistro.transaccion_id.sIdTransaccion,
                    oRegistro.transaccion_id.tipo_transaccion_id.sCodigo,
                ))
