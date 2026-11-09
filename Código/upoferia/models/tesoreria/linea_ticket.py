from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LineaTicket(models.Model):

    _name = 'upoferia.linea_ticket'
    _description = 'Línea de ticket'

    iNumeroLinea = fields.Integer(string="Nº de línea", required=True, help="Identifica la línea dentro de su ticket")
    iCantidad = fields.Integer(string="Cantidad", required=True, default=1)
    fPrecioUnitario = fields.Float(string="Precio unitario", required=True, digits=(10, 2))
    
    # Relaciones
    ticket_id = fields.Many2one('upoferia.ticket', string="Ticket", required=True)
    producto_id = fields.Many2one('upoferia.producto', string="Producto", required=True)

    _sql_constraints = [
        ('numero_linea_ticket_unique', 'UNIQUE("ticket_id", "iNumeroLinea")',
         'Ya existe una línea con ese número en este ticket.'),
    ]

    @api.constrains('iNumeroLinea')
    def _check_numero_linea(self):
        for record in self:
            if record.iNumeroLinea <= 0:
                raise ValidationError('El número de línea debe ser mayor que 0.')

    @api.constrains('iCantidad')
    def _check_cantidad(self):
        for record in self:
            if record.iCantidad <= 0:
                raise ValidationError('La cantidad debe ser mayor que 0.')

    @api.constrains('fPrecioUnitario')
    def _check_precio_unitario(self):
        for record in self:
            if record.fPrecioUnitario < 0:
                raise ValidationError('El precio unitario no puede ser negativo.')

    @api.onchange('iCantidad')
    def onchange_cantidad(self):
        if self.iCantidad < 1:
            return {
                'value': {'iCantidad': 1},
                'warning': {
                    'title': 'Cantidad incorrecta',
                    'message': 'La cantidad mínima es 1.'
                }
            }
        if self.iCantidad > 50:
            return {
                'warning': {
                    'title': 'Cantidad elevada',
                    'message': 'Se van a cobrar %s unidades en una sola línea. Comprueba que es correcto.' % self.iCantidad
                }
            }

    @api.onchange('fPrecioUnitario')
    def onchange_precio_unitario(self):
        if self.fPrecioUnitario == 0:
            return {
                'warning': {
                    'title': 'Precio a cero',
                    'message': 'La línea tiene precio 0 €. Si es una invitación es correcto; si no, revisa el precio.'
                }
            }