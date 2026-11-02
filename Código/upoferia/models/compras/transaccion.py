from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Transaccion(models.Model):
    _name = 'feria.transaccion'
    _description = 'Transacción con proveedor'
    _rec_name = 'sIdTransaccion'
    _sql_constraints = [
        ('id_transaccion_uniq', 'UNIQUE ("sIdTransaccion")',
         'Ya existe una transacción con ese identificador.'),
    ]

    sIdTransaccion = fields.Char(string='Id. transacción', required=True)
    fImporte = fields.Float(string='Importe')
    sEstado = fields.Selection(
        selection=[
            ('borrador', 'Borrador'),
            ('confirmado', 'Confirmado'),
            ('recibido', 'Recibido'),
            ('cancelado', 'Cancelado'),
            ('previsto', 'Previsto'),
            ('hecho', 'Hecho'),
            ('pendiente', 'Pendiente'),
            ('pagada', 'Pagada'),
            ('vencida', 'Vencida'),
            ('vigente', 'Vigente'),
            ('vencido', 'Vencido'),
            ('rescindido', 'Rescindido'),
        ],
        string='Estado',
    )
    dFechaInicial = fields.Date(string='Fecha inicial')
    dVencimiento = fields.Date(string='Vencimiento')
    dFechaPrevistaFin = fields.Date(string='Fecha prevista de fin')
    bRenovacionAuto = fields.Boolean(string='Renovación automática')
    sDocumento = fields.Char(string='Documento')
    sRefProveedor = fields.Char(string='Referencia del proveedor')

    @api.constrains('sIdTransaccion')
    def _check_id_transaccion_obligatorio(self):
        oRegistro = None
        for oRegistro in self:
            if not (oRegistro.sIdTransaccion or '').strip():
                raise ValidationError('El campo «Id. transacción» es obligatorio.')

    @api.constrains('fImporte')
    def _check_importe(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.fImporte < 0:
                raise ValidationError('«Importe» no puede ser menor que 0.')

    @api.constrains('dFechaInicial', 'dVencimiento')
    def _check_vencimiento(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.dFechaInicial and oRegistro.dVencimiento and oRegistro.dVencimiento < oRegistro.dFechaInicial:
                raise ValidationError('«Vencimiento» no puede ser anterior a «Fecha inicial».')

    @api.constrains('dFechaInicial', 'dFechaPrevistaFin')
    def _check_fecha_prevista_fin(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.dFechaInicial and oRegistro.dFechaPrevistaFin and oRegistro.dFechaPrevistaFin < oRegistro.dFechaInicial:
                raise ValidationError('«Fecha prevista de fin» no puede ser anterior a «Fecha inicial».')

    @api.onchange('dFechaInicial', 'dVencimiento', 'dFechaPrevistaFin')
    def _onchange_valores(self):
        sMensaje = False
        if self.dFechaInicial and self.dVencimiento and self.dVencimiento < self.dFechaInicial:
            sMensaje = '«Vencimiento» no puede ser anterior a «Fecha inicial».'
        if not sMensaje and self.dFechaInicial and self.dFechaPrevistaFin and self.dFechaPrevistaFin < self.dFechaInicial:
            sMensaje = '«Fecha prevista de fin» no puede ser anterior a «Fecha inicial».'
        if sMensaje:
            return {
                'warning': {
                    'title': 'Valores incorrectos',
                    'message': sMensaje,
                }
            }
