from odoo import models, fields, api


class LineaPresupuesto(models.Model):

    _name = 'upoferia.linea_presupuesto'
    _description = 'Línea de presupuesto'
    _rec_name = 'sConcepto'

    sConcepto = fields.Char(string="Concepto", required=True, help="Identifica la línea dentro de su presupuesto")
    selTipo = fields.Selection([('ingreso', 'Ingreso'),
                             ('gasto', 'Gasto'),],
                            'Tipo', required=True)
    fImportePrevisto = fields.Float(string="Importe previsto", required=True, digits=(10, 2))
    
    # Relaciones
    presupuesto_id = fields.Many2one('upoferia.presupuesto', string="Presupuesto", required=True)
    categoria_economica_id = fields.Many2one('upoferia.categoria_economica', string="Categoría económica", required=True)
    movimiento_ids = fields.One2many('upoferia.movimiento', 'linea_presupuesto_id', string="Movimientos")
    # Relaciones con modelos de otro grupo
    # PENDIENTE (modelo no existe): transaccion_ids = fields.One2many('upoferia.transaccion', 'linea_presupuesto_id', string="Transacciones")  # TRANSACCION (ejercicio_presupuesto, concepto_linea_presupuesto)

    _sql_constraints = [
        ('concepto_presupuesto_unique', 'UNIQUE("presupuesto_id", "sConcepto")',
         'Ya existe una línea con ese concepto en este presupuesto.'),
    ]

    @api.constrains('sConcepto')
    def _check_concepto(self):
        for record in self:
            if not record.sConcepto.strip():
                raise models.ValidationError('El concepto de la línea de presupuesto no puede estar vacío.')

    @api.constrains('fImportePrevisto')
    def _check_importe_previsto(self):
        for record in self:
            if record.fImportePrevisto < 0:
                raise models.ValidationError('El importe previsto no puede ser negativo; indica si es ingreso o gasto '
                                      'con el campo «Tipo».')

    @api.onchange('fImportePrevisto')
    def onchange_importe_previsto(self):
        if self.fImportePrevisto < 0:
            return {
                'value': {'fImportePrevisto': abs(self.fImportePrevisto)},
                'warning': {
                    'title': 'Importe negativo',
                    'message': 'El importe se guarda siempre en positivo. Para un gasto, elige «Gasto» en el campo «Tipo».'
                }
            }
        if self.fImportePrevisto == 0:
            return {
                'warning': {
                    'title': 'Importe a cero',
                    'message': 'La línea tiene un importe previsto de 0 €. Comprueba que es correcto.'
                }
            }