from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Bonificacion(models.Model):

    _name = 'upoferia.bonificacion'
    _description = 'Bonificación aplicable a cuotas'
    _rec_name = 'sNombre'

    sNombre = fields.Char(string="Nombre", required=True, help="Identificador único de la bonificación")
    fPorcentajeDescuento = fields.Float(string="Porcentaje de descuento", required=True, digits=(5, 2))
    
    # Relaciones
    cuota_ids = fields.One2many('upoferia.cuota', 'bonificacion_id', string="Cuotas")

    _sql_constraints = [
        ('nombre_unique', 'UNIQUE("sNombre")', 'Ya existe una bonificación con ese nombre.'),
    ]

    @api.constrains('sNombre')
    def _check_nombre(self):
        for record in self:
            if not record.sNombre.strip():
                raise ValidationError('El nombre de la bonificación no puede estar vacío.')

    @api.constrains('fPorcentajeDescuento')
    def _check_porcentaje_descuento(self):
        for record in self:
            if not (0 < record.fPorcentajeDescuento <= 100):
                raise ValidationError('El porcentaje de descuento debe estar entre 0 y 100.')

    @api.onchange('fPorcentajeDescuento')
    def onchange_porcentaje_descuento(self):
        if self.fPorcentajeDescuento == 100:
            return {
                'warning': {
                    'title': 'Bonificación total',
                    'message': 'Un descuento del 100 % deja la cuota a 0 €. Comprueba que es correcto.'
                }
            }
        if self.fPorcentajeDescuento > 50:
            return {
                'warning': {
                    'title': 'Descuento elevado',
                    'message': 'El descuento supera el 50 %. Comprueba que es correcto.'
                }
            }