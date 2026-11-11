from odoo import models, fields, api

TIPOS_CON_PERIODO = ('liquidacion_cuenta', 'nomina')


class Movimiento(models.Model):

    _name = 'upoferia.movimiento'
    _description = 'Movimiento de tesorería'
    _rec_name = 'sReferencia'

    sReferencia = fields.Char(string="Referencia", required=True, help="Identificador único del movimiento")
    dFecha = fields.Date(string="Fecha", required=True)
    fImporte = fields.Float(string="Importe", required=True, digits=(10, 2))
    selEstado = fields.Selection([('borrador', 'Borrador'),
                               ('confirmado', 'Confirmado'),
                               ('anulado', 'Anulado'),],
                              'Estado', default='borrador')
    selTipo = fields.Selection([('cuota_socio', 'Cuota de socio'),
                             ('consumo_barra', 'Consumo en barra'),
                             ('liquidacion_cuenta', 'Liquidación de cuenta'),
                             ('nomina', 'Nómina'),
                             ('gasto_adelantado', 'Gasto adelantado'),
                             ('pago_proveedor', 'Pago a proveedor'),
                             ('cobro_cliente', 'Cobro a cliente'),],
                            'Tipo', required=True)
    sPeriodo = fields.Char(string="Periodo")
    sConcepto = fields.Char(string="Concepto")

    # Relaciones
    cuota_id = fields.Many2one('upoferia.cuota', string="Cuota")
    ticket_id = fields.Many2one('upoferia.ticket', string="Ticket")
    linea_presupuesto_id = fields.Many2one('upoferia.linea_presupuesto', string="Línea de presupuesto")
    metodo_pago_id = fields.Many2one('upoferia.metodo_pago', string="Método de pago", required=True)
    cuenta_bancaria_id = fields.Many2one('upoferia.cuenta_bancaria', string="Cuenta bancaria")
    caja_id = fields.Many2one('upoferia.caja', string="Caja")
    categoria_economica_id = fields.Many2one('upoferia.categoria_economica', string="Categoría económica")
    liquidacion_id = fields.Many2one('upoferia.movimiento', string="Liquidación",
                                     help="Movimiento de liquidación de cuenta en el que se incluye este movimiento")
    movimiento_liquidado_ids = fields.One2many('upoferia.movimiento', 'liquidacion_id', string="Movimientos liquidados")
    # Relaciones con modelos de otro grupo
    socio_id = fields.Many2one('upoferia.socios.socio', string="Socio")  # SOCIO (dni_socio)
    transaccion_id = fields.Many2one('upoferia.transaccion', string="Transacción")  # TRANSACCION (id_transaccion)
    empleado_id = fields.Many2one('upoferia.rrhh.empleado', string="Empleado")  # EMPLEADO (dni_empleado)
    # FICHAJE (referencia_nomina): pendiente de que upoferia.turnos.fichaje tenga un Many2one nomina_id
    # hacia upoferia.movimiento; hoy solo tiene referencia_nomina (Char) y el One2many rompería la instalación.
    # fichaje_ids = fields.One2many('upoferia.turnos.fichaje', 'nomina_id', string="Fichajes retribuidos")

    _sql_constraints = [
        ('referencia_unique', 'UNIQUE("sReferencia")', 'Ya existe un movimiento con esa referencia.'),
    ]

    @api.constrains('sReferencia')
    def _check_referencia(self):
        for record in self:
            if not record.sReferencia.strip():
                raise models.ValidationError('La referencia del movimiento no puede estar vacía.')

    @api.constrains('fImporte')
    def _check_importe(self):
        for record in self:
            if record.fImporte <= 0:
                raise models.ValidationError('El importe debe ser mayor que 0; si es ingreso o gasto lo indica el tipo '
                                      'de movimiento.')

    @api.constrains('ticket_id')
    def _check_ticket(self):
        for record in self.filtered('ticket_id'):
            if self.search_count([('ticket_id', '=', record.ticket_id.id), ('id', '!=', record.id)]):
                raise models.ValidationError('Ese ticket ya está asociado a otro movimiento.')

    @api.constrains('selTipo', 'sPeriodo')
    def _check_periodo(self):
        for record in self:
            if record.selTipo in TIPOS_CON_PERIODO and not (record.sPeriodo or '').strip():
                raise models.ValidationError('Los movimientos de tipo «%s» deben indicar el periodo que cubren.'
                                      % dict(self._fields['selTipo'].selection).get(record.selTipo))

    @api.constrains('selTipo', 'sConcepto')
    def _check_concepto(self):
        for record in self:
            if record.selTipo == 'gasto_adelantado' and not (record.sConcepto or '').strip():
                raise models.ValidationError('Un gasto adelantado debe indicar en el concepto en qué se ha gastado el dinero.')

    @api.constrains('selEstado', 'dFecha')
    def _check_fecha_confirmado(self):
        for record in self:
            if record.selEstado == 'confirmado' and record.dFecha > fields.Date.context_today(record):
                raise models.ValidationError('No se puede confirmar un movimiento con fecha futura (%s).' % record.dFecha)

    @api.onchange('fImporte')
    def onchange_importe(self):
        if self.fImporte < 0:
            return {
                'value': {'fImporte': abs(self.fImporte)},
                'warning': {
                    'title': 'Importe negativo',
                    'message': 'El importe se guarda siempre en positivo; si es ingreso o gasto lo indica el tipo.'
                }
            }

    @api.onchange('selTipo')
    def onchange_tipo(self):
        if self.selTipo in TIPOS_CON_PERIODO and not self.sPeriodo:
            return {
                'warning': {
                    'title': 'Falta el periodo',
                    'message': 'Este tipo de movimiento necesita el periodo que cubre (por ejemplo, «Abril 2026»).'
                }
            }
        if self.selTipo not in TIPOS_CON_PERIODO and self.sPeriodo:
            self.sPeriodo = False

    @api.onchange('selEstado')
    def onchange_estado(self):
        if self._origin.id and self._origin.selEstado == 'anulado' and self.selEstado != 'anulado':
            return {
                'value': {'selEstado': 'anulado'},
                'warning': {
                    'title': 'Movimiento anulado',
                    'message': 'Un movimiento anulado no puede reactivarse. Crea un movimiento nuevo.'
                }
            }