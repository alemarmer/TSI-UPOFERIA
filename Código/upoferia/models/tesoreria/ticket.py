from odoo import models, fields


class Ticket(models.Model):

    _name = 'upoferia.ticket'
    _description = 'Ticket de consumición'
    _rec_name = 'referencia'

    referencia = fields.Char(string="Referencia", required=True, help="Identificador único del ticket")
    fecha = fields.Datetime(string="Fecha", required=True, default=fields.Datetime.now)
    
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