from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Actuacion(models.Model):
    _inherit = 'upoferia.actuacion'

    transaccion_id = fields.Many2one('feria.transaccion', string='Contrato', ondelete='set null')

    @api.constrains('transaccion_id')
    def _check_transaccion(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.transaccion_id and oRegistro.transaccion_id.tipo_transaccion_id.sCodigo != 'CON':
                raise ValidationError('Una actuación solo se puede asociar a un contrato (CON); %s es %s.' % (
                    oRegistro.transaccion_id.sIdTransaccion,
                    oRegistro.transaccion_id.tipo_transaccion_id.sCodigo,
                ))
