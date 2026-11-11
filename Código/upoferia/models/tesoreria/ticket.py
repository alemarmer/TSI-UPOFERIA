from odoo import models, fields, api


class Ticket(models.Model):

    _name = 'upoferia.ticket'
    _description = 'Ticket de consumición'
    _rec_name = 'sReferencia'

    sReferencia = fields.Char(string="Referencia", required=True, help="Identificador único del ticket")
    dtFecha = fields.Datetime(string="Fecha", required=True, default=fields.Datetime.now)
    
    # Relaciones
    tarifa_id = fields.Many2one('upoferia.tarifa', string="Tarifa", required=True)
    linea_ids = fields.One2many('upoferia.linea_ticket', 'ticket_id', string="Líneas del ticket")
    movimiento_ids = fields.One2many('upoferia.movimiento', 'ticket_id', string="Movimiento")

    _sql_constraints = [
        ('referencia_unique', 'UNIQUE("sReferencia")', 'Ya existe un ticket con esa referencia.'),
    ]

    @api.constrains('sReferencia')
    def _check_referencia(self):
        for record in self:
            if not record.sReferencia.strip():
                raise models.ValidationError('La referencia del ticket no puede estar vacía.')

    @api.constrains('dtFecha')
    def _check_fecha(self):
        ahora = fields.Datetime.now()
        for record in self:
            if record.dtFecha > ahora:
                raise models.ValidationError('Un ticket no puede tener fecha futura (%s).' % record.dtFecha)

    @api.onchange('dtFecha')
    def onchange_fecha(self):
        if self.dtFecha and self.dtFecha > fields.Datetime.now():
            return {
                'value': {'dtFecha': fields.Datetime.now()},
                'warning': {
                    'title': 'Fecha futura',
                    'message': 'Un ticket se registra en el momento de la venta; se ha puesto la fecha y hora actuales.'
                }
            }