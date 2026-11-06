from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Ticket(models.Model):

    _name = 'upoferia.ticket'
    _description = 'Ticket de consumición'
    _rec_name = 'referencia'

    referencia = fields.Char(string="Referencia", required=True, help="Identificador único del ticket")
    fecha = fields.Datetime(string="Fecha", required=True, default=fields.Datetime.now)
    
    # Relaciones
    tarifa_id = fields.Many2one('upoferia.tarifa', string="Tarifa", required=True, ondelete='restrict')
    linea_ids = fields.One2many('upoferia.linea_ticket', 'ticket_id', string="Líneas del ticket")
    movimiento_ids = fields.One2many('upoferia.movimiento', 'ticket_id', string="Movimiento")

    _sql_constraints = [
        ('referencia_unique', 'UNIQUE(referencia)', 'Ya existe un ticket con esa referencia.'),
    ]

    @api.constrains('referencia')
    def _check_referencia(self):
        for record in self:
            if not record.referencia.strip():
                raise ValidationError('La referencia del ticket no puede estar vacía.')

    @api.constrains('fecha')
    def _check_fecha(self):
        ahora = fields.Datetime.now()
        for record in self:
            if record.fecha > ahora:
                raise ValidationError('Un ticket no puede tener fecha futura (%s).' % record.fecha)

    @api.onchange('fecha')
    def onchange_fecha(self):
        if self.fecha and self.fecha > fields.Datetime.now():
            return {
                'value': {'fecha': fields.Datetime.now()},
                'warning': {
                    'title': 'Fecha futura',
                    'message': 'Un ticket se registra en el momento de la venta; se ha puesto la fecha y hora actuales.'
                }
            }