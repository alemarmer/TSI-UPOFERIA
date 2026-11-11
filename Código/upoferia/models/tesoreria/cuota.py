from odoo import models, fields, api
from datetime import timedelta


class Cuota(models.Model):

    _name = 'upoferia.cuota'
    _description = 'Cuota de socio'
    _rec_name = 'sReferencia'

    sReferencia = fields.Char(string="Referencia", required=True, help="Identificador único de la cuota")
    iEjercicio = fields.Integer(string="Ejercicio", required=True)
    dFechaEmision = fields.Date(string="Fecha de emisión", required=True)
    dFechaVencimiento = fields.Date(string="Fecha de vencimiento", required=True)
    selPeriodicidad = fields.Selection([('anual', 'Anual'),
                                     ('mensual', 'Mensual'),
                                     ('unica', 'Única'),],
                                    'Periodicidad', default='anual')
    
    # Relaciones
    tipo_cuota_id = fields.Many2one('upoferia.tipo_cuota', string="Tipo de cuota", required=True)
    bonificacion_id = fields.Many2one('upoferia.bonificacion', string="Bonificación")
    movimiento_ids = fields.One2many('upoferia.movimiento', 'cuota_id', string="Movimientos")
    # Relaciones con modelos de otro grupo
    socio_id = fields.Many2one('upoferia.socios.socio', string="Socio", required=True)  # SOCIO (dni_socio)

    _sql_constraints = [
        ('referencia_unique', 'UNIQUE("sReferencia")', 'Ya existe una cuota con esa referencia.'),
    ]

    @api.constrains('sReferencia')
    def _check_referencia(self):
        for record in self:
            if not record.sReferencia.strip():
                raise models.ValidationError('La referencia de la cuota no puede estar vacía.')

    @api.constrains('iEjercicio', 'dFechaEmision')
    def _check_ejercicio(self):
        for record in self:
            if not (2000 <= record.iEjercicio <= 2100):
                raise models.ValidationError('El ejercicio debe ser un año válido (2000-2100).')
            if abs(record.dFechaEmision.year - record.iEjercicio) > 1:
                raise models.ValidationError('La fecha de emisión (%s) no corresponde al ejercicio %s.'
                                      % (record.dFechaEmision, record.iEjercicio))

    @api.constrains('dFechaEmision', 'dFechaVencimiento')
    def _check_fechas(self):
        for record in self:
            if record.dFechaVencimiento < record.dFechaEmision:
                raise models.ValidationError('La fecha de vencimiento no puede ser anterior a la de emisión.')

    @api.onchange('dFechaEmision')
    def onchange_fecha_emision(self):
        if self.dFechaEmision:
            if not self.iEjercicio:
                self.iEjercicio = self.dFechaEmision.year
            if not self.dFechaVencimiento:
                self.dFechaVencimiento = self.dFechaEmision + timedelta(days=30)

    @api.onchange('dFechaEmision', 'dFechaVencimiento')
    def onchange_fechas(self):
        if self.dFechaEmision and self.dFechaVencimiento and self.dFechaVencimiento < self.dFechaEmision:
            return {
                'value': {'dFechaVencimiento': self.dFechaEmision + timedelta(days=30)},
                'warning': {
                    'title': 'Fechas incorrectas',
                    'message': 'El vencimiento era anterior a la emisión; se ha puesto a 30 días desde la emisión.'
                }
            }