from odoo import models, fields


class Movimiento(models.Model):

    _name = 'upoferia.movimiento'
    _description = 'Movimiento de tesorería'
    _rec_name = 'referencia'

    referencia = fields.Char(string="Referencia", required=True, help="Identificador único del movimiento")
    fecha = fields.Date(string="Fecha", required=True)
    importe = fields.Float(string="Importe", required=True, digits=(10, 2))
    estado = fields.Selection([('borrador', 'Borrador'),
                               ('confirmado', 'Confirmado'),
                               ('anulado', 'Anulado'),],
                              'Estado', default='borrador')
    tipo = fields.Selection([('cuota_socio', 'Cuota de socio'),
                             ('consumo_barra', 'Consumo en barra'),
                             ('liquidacion_cuenta', 'Liquidación de cuenta'),
                             ('nomina', 'Nómina'),
                             ('gasto_adelantado', 'Gasto adelantado'),
                             ('pago_proveedor', 'Pago a proveedor'),
                             ('cobro_cliente', 'Cobro a cliente'),],
                            'Tipo', required=True)
    periodo = fields.Char(string="Periodo")
    concepto = fields.Char(string="Concepto")
    
    _sql_constraints = [
        ('referencia_unique', 'UNIQUE(referencia)', 'Ya existe un movimiento con esa referencia.'),
        ('importe_positivo', 'CHECK(importe > 0)',
         'El importe debe ser mayor que 0; si es ingreso o gasto lo indica el tipo de movimiento.'),
    ]

    @api.constrains('referencia')
    def _check_referencia(self):
        for record in self:
            if not record.referencia.strip():
                raise ValidationError('La referencia del movimiento no puede estar vacía.')

    @api.constrains('tipo', 'periodo')
    def _check_periodo(self):
        for record in self:
            if record.tipo in self.TIPOS_CON_PERIODO and not (record.periodo or '').strip():
                raise ValidationError('Los movimientos de tipo «%s» deben indicar el periodo que cubren.'
                                      % dict(self._fields['tipo'].selection).get(record.tipo))

    @api.constrains('tipo', 'concepto')
    def _check_concepto(self):
        for record in self:
            if record.tipo == 'gasto_adelantado' and not (record.concepto or '').strip():
                raise ValidationError('Un gasto adelantado debe indicar en el concepto en qué se ha gastado el dinero.')

    @api.constrains('estado', 'fecha')
    def _check_fecha_confirmado(self):
        for record in self:
            if record.estado == 'confirmado' and record.fecha > fields.Date.context_today(record):
                raise ValidationError('No se puede confirmar un movimiento con fecha futura (%s).' % record.fecha)

    @api.onchange('importe')
    def onchange_importe(self):
        if self.importe < 0:
            return {
                'value': {'importe': abs(self.importe)},
                'warning': {
                    'title': 'Importe negativo',
                    'message': 'El importe se guarda siempre en positivo; si es ingreso o gasto lo indica el tipo.'
                }
            }

    @api.onchange('tipo')
    def onchange_tipo(self):
        if self.tipo in self.TIPOS_CON_PERIODO and not self.periodo:
            return {
                'warning': {
                    'title': 'Falta el periodo',
                    'message': 'Este tipo de movimiento necesita el periodo que cubre (por ejemplo, «Abril 2026»).'
                }
            }
        if self.tipo not in self.TIPOS_CON_PERIODO and self.periodo:
            self.periodo = False

    @api.onchange('estado')
    def onchange_estado(self):
        if self._origin.id and self._origin.estado == 'anulado' and self.estado != 'anulado':
            return {
                'value': {'estado': 'anulado'},
                'warning': {
                    'title': 'Movimiento anulado',
                    'message': 'Un movimiento anulado no puede reactivarse. Crea un movimiento nuevo.'
                }
            }
