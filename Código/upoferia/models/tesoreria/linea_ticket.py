from odoo import models, fields


class LineaTicket(models.Model):

    _name = 'upoferia.linea_ticket'
    _description = 'Línea de ticket'

    numero_linea = fields.Integer(string="Nº de línea", required=True, help="Identifica la línea dentro de su ticket")
    cantidad = fields.Integer(string="Cantidad", required=True, default=1)
    precio_unitario = fields.Float(string="Precio unitario", required=True, digits=(10, 2))
    
    _sql_constraints = [
        ('numero_linea_positivo', 'CHECK(numero_linea > 0)', 'El número de línea debe ser mayor que 0.'),
        ('cantidad_positiva', 'CHECK(cantidad > 0)', 'La cantidad debe ser mayor que 0.'),
        ('precio_no_negativo', 'CHECK(precio_unitario >= 0)', 'El precio unitario no puede ser negativo.'),
    ]

    @api.onchange('cantidad')
    def onchange_cantidad(self):
        if self.cantidad < 1:
            return {
                'value': {'cantidad': 1},
                'warning': {
                    'title': 'Cantidad incorrecta',
                    'message': 'La cantidad mínima es 1.'
                }
            }
        if self.cantidad > 50:
            return {
                'warning': {
                    'title': 'Cantidad elevada',
                    'message': 'Se van a cobrar %s unidades en una sola línea. Comprueba que es correcto.' % self.cantidad
                }
            }

    @api.onchange('precio_unitario')
    def onchange_precio_unitario(self):
        if self.precio_unitario == 0:
            return {
                'warning': {
                    'title': 'Precio a cero',
                    'message': 'La línea tiene precio 0 €. Si es una invitación es correcto; si no, revisa el precio.'
                }
            }