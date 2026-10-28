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
    
    _sql_constraints = [
        ('importe_previsto_positivo', 'CHECK(importe_previsto >= 0)',
         'El importe previsto no puede ser negativo; indica si es ingreso o gasto con el campo «Tipo».'),
    ]

    @api.constrains('concepto')
    def _check_concepto(self):
        for record in self:
            if not record.concepto.strip():
                raise ValidationError('El concepto de la línea de presupuesto no puede estar vacío.')

    @api.onchange('importe_previsto')
    def onchange_importe_previsto(self):
        if self.importe_previsto < 0:
            return {
                'value': {'importe_previsto': abs(self.importe_previsto)},
                'warning': {
                    'title': 'Importe negativo',
                    'message': 'El importe se guarda siempre en positivo. Para un gasto, elige «Gasto» en el campo «Tipo».'
                }
            }
        if self.importe_previsto == 0:
            return {
                'warning': {
                    'title': 'Importe a cero',
                    'message': 'La línea tiene un importe previsto de 0 €. Comprueba que es correcto.'
                }
            }