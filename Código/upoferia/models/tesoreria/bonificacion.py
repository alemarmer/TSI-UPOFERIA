from odoo import models, fields


class Bonificacion(models.Model):

    _name = 'upoferia.bonificacion'
    _description = 'Bonificación aplicable a cuotas'
    _rec_name = 'nombre'

    nombre = fields.Char(string="Nombre", required=True, help="Identificador único de la bonificación")
    porcentaje_descuento = fields.Float(string="Porcentaje de descuento", required=True, digits=(5, 2))
    
    _sql_constraints = [
        ('nombre_unique', 'UNIQUE(nombre)', 'Ya existe una bonificación con ese nombre.'),
        ('porcentaje_rango', 'CHECK(porcentaje_descuento > 0 AND porcentaje_descuento <= 100)',
         'El porcentaje de descuento debe estar entre 0 y 100.'),
    ]

    @api.constrains('nombre')
    def _check_nombre(self):
        for record in self:
            if not record.nombre.strip():
                raise ValidationError('El nombre de la bonificación no puede estar vacío.')

    @api.onchange('porcentaje_descuento')
    def onchange_porcentaje_descuento(self):
        if self.porcentaje_descuento == 100:
            return {
                'warning': {
                    'title': 'Bonificación total',
                    'message': 'Un descuento del 100 % deja la cuota a 0 €. Comprueba que es correcto.'
                }
            }
        if self.porcentaje_descuento > 50:
            return {
                'warning': {
                    'title': 'Descuento elevado',
                    'message': 'El descuento supera el 50 %. Comprueba que es correcto.'
                }
            }