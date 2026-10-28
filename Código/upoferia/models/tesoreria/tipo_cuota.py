from odoo import models, fields


class TipoCuota(models.Model):

    _name = 'upoferia.tipo_cuota'
    _description = 'Tipo de cuota'
    _rec_name = 'nombre'

    nombre = fields.Char(string="Nombre", required=True, help="Identificador único del tipo de cuota")
    importe = fields.Float(string="Importe", required=True, digits=(10, 2))
    
    _sql_constraints = [
        ('nombre_unique', 'UNIQUE(nombre)', 'Ya existe un tipo de cuota con ese nombre.'),
        ('importe_positivo', 'CHECK(importe > 0)', 'El importe del tipo de cuota debe ser mayor que 0.'),
    ]

    @api.constrains('nombre')
    def _check_nombre(self):
        for record in self:
            if not record.nombre.strip():
                raise ValidationError('El nombre del tipo de cuota no puede estar vacío.')

    @api.onchange('importe')
    def onchange_importe(self):
        if self.importe < 0:
            return {
                'value': {'importe': abs(self.importe)},
                'warning': {
                    'title': 'Importe negativo',
                    'message': 'El importe de una cuota no puede ser negativo; se ha pasado a positivo.'
                }
            }
        if self._origin.id and self._origin.importe and self.importe != self._origin.importe:
            return {
                'warning': {
                    'title': 'Cambio de importe',
                    'message': 'El importe pasa de %.2f € a %.2f €. Afectará a las cuotas que se emitan a partir de ahora, '
                               'no a las ya emitidas.' % (self._origin.importe, self.importe)
                }
            }