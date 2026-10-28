from odoo import models, fields


class LineaPresupuesto(models.Model):

    _name = 'upoferia.linea_presupuesto'
    _description = 'Línea de presupuesto'
    _rec_name = 'concepto'

    concepto = fields.Char(string="Concepto", required=True, help="Identifica la línea dentro de su presupuesto")
    tipo = fields.Selection([('ingreso', 'Ingreso'),
                             ('gasto', 'Gasto'),],
                            'Tipo', required=True)
    importe_previsto = fields.Float(string="Importe previsto", required=True, digits=(10, 2))