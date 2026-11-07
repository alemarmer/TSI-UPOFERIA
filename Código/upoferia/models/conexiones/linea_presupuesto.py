from odoo import models, fields


class LineaPresupuesto(models.Model):
    _inherit = 'upoferia.linea_presupuesto'

    transaccion_ids = fields.One2many('feria.transaccion', 'linea_presupuesto_id', string='Contratos')
