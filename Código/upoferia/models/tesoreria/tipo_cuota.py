from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TipoCuota(models.Model):

    _name = 'upoferia.tipo_cuota'
    _description = 'Tipo de cuota'
    _rec_name = 'sNombre'

    sNombre = fields.Char(string="Nombre", required=True, help="Identificador único del tipo de cuota")
    fImporte = fields.Float(string="Importe", required=True, digits=(10, 2))
    
    # Relaciones
    cuota_ids = fields.One2many('upoferia.cuota', 'tipo_cuota_id', string="Cuotas")

    _sql_constraints = [
        ('nombre_unique', 'UNIQUE("sNombre")', 'Ya existe un tipo de cuota con ese nombre.'),
    ]

    @api.constrains('sNombre')
    def _check_nombre(self):
        for record in self:
            if not record.sNombre.strip():
                raise ValidationError('El nombre del tipo de cuota no puede estar vacío.')

    @api.constrains('fImporte')
    def _check_importe(self):
        for record in self:
            if record.fImporte <= 0:
                raise ValidationError('El importe del tipo de cuota debe ser mayor que 0.')

    @api.onchange('fImporte')
    def onchange_importe(self):
        if self.fImporte < 0:
            return {
                'value': {'fImporte': abs(self.fImporte)},
                'warning': {
                    'title': 'Importe negativo',
                    'message': 'El importe de una cuota no puede ser negativo; se ha pasado a positivo.'
                }
            }
        if self._origin.id and self._origin.fImporte and self.fImporte != self._origin.fImporte:
            return {
                'warning': {
                    'title': 'Cambio de importe',
                    'message': 'El importe pasa de %.2f € a %.2f €. Afectará a las cuotas que se emitan a partir de ahora, '
                               'no a las ya emitidas.' % (self._origin.fImporte, self.fImporte)
                }
            }