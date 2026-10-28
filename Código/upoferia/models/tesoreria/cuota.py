from odoo import models, fields


class Cuota(models.Model):

    _name = 'upoferia.cuota'
    _description = 'Cuota de socio'
    _rec_name = 'referencia'

    referencia = fields.Char(string="Referencia", required=True, help="Identificador único de la cuota")
    ejercicio = fields.Integer(string="Ejercicio", required=True)
    fecha_emision = fields.Date(string="Fecha de emisión", required=True)
    fecha_vencimiento = fields.Date(string="Fecha de vencimiento", required=True)
    periodicidad = fields.Selection([('anual', 'Anual'),
                                     ('mensual', 'Mensual'),
                                     ('unica', 'Única'),],
                                    'Periodicidad', default='anual')
    
    _sql_constraints = [
        ('referencia_unique', 'UNIQUE(referencia)', 'Ya existe una cuota con esa referencia.'),
        ('ejercicio_rango', 'CHECK(ejercicio BETWEEN 2000 AND 2100)', 'El ejercicio debe ser un año válido (2000-2100).'),
        ('fechas_orden', 'CHECK(fecha_vencimiento >= fecha_emision)',
         'La fecha de vencimiento no puede ser anterior a la de emisión.'),
    ]

    @api.constrains('referencia')
    def _check_referencia(self):
        for record in self:
            if not record.referencia.strip():
                raise ValidationError('La referencia de la cuota no puede estar vacía.')

    @api.constrains('ejercicio', 'fecha_emision')
    def _check_ejercicio(self):
        for record in self:
            if abs(record.fecha_emision.year - record.ejercicio) > 1:
                raise ValidationError('La fecha de emisión (%s) no corresponde al ejercicio %s.'
                                      % (record.fecha_emision, record.ejercicio))

    @api.onchange('fecha_emision')
    def onchange_fecha_emision(self):
        if self.fecha_emision:
            if not self.ejercicio:
                self.ejercicio = self.fecha_emision.year
            if not self.fecha_vencimiento:
                self.fecha_vencimiento = self.fecha_emision + timedelta(days=30)

    @api.onchange('fecha_emision', 'fecha_vencimiento')
    def onchange_fechas(self):
        if self.fecha_emision and self.fecha_vencimiento and self.fecha_vencimiento < self.fecha_emision:
            return {
                'value': {'fecha_vencimiento': self.fecha_emision + timedelta(days=30)},
                'warning': {
                    'title': 'Fechas incorrectas',
                    'message': 'El vencimiento era anterior a la emisión; se ha puesto a 30 días desde la emisión.'
                }
            }