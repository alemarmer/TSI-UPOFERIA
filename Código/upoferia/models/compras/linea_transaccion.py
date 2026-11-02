from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LineaTransaccion(models.Model):
    _name = 'feria.linea_transaccion'
    _description = 'Línea de transacción'
    _rec_name = 'iNumeroLinea'

    iNumeroLinea = fields.Integer(string='Número de línea', required=True)
    iCantidad = fields.Integer(string='Cantidad')
    iCantidadRecibida = fields.Integer(string='Cantidad recibida')
    fPrecioUnitario = fields.Float(string='Precio unitario')

    @api.constrains('iNumeroLinea')
    def _check_numero_linea(self):
        oRegistro = None
        for oRegistro in self:
            if not 1 <= oRegistro.iNumeroLinea <= 9999:
                raise ValidationError('«Número de línea» debe estar entre 1 y 9999.')

    @api.constrains('iCantidad')
    def _check_cantidad(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.iCantidad <= 0:
                raise ValidationError('«Cantidad» debe ser mayor que 0.')

    @api.constrains('iCantidadRecibida')
    def _check_cantidad_recibida(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.iCantidadRecibida < 0:
                raise ValidationError('«Cantidad recibida» no puede ser menor que 0.')

    @api.constrains('iCantidadRecibida', 'iCantidad')
    def _check_cantidad_recibida_cantidad(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.iCantidadRecibida > oRegistro.iCantidad:
                raise ValidationError('«Cantidad recibida» no puede superar «Cantidad».')

    @api.constrains('fPrecioUnitario')
    def _check_precio_unitario(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.fPrecioUnitario < 0:
                raise ValidationError('«Precio unitario» no puede ser menor que 0.')

    @api.onchange('iCantidadRecibida', 'iCantidad')
    def _onchange_valores(self):
        sMensaje = False
        if self.iCantidadRecibida > self.iCantidad:
            sMensaje = '«Cantidad recibida» no puede superar «Cantidad».'
        if sMensaje:
            return {
                'warning': {
                    'title': 'Valores incorrectos',
                    'message': sMensaje,
                }
            }
