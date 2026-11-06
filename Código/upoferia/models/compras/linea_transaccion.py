from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LineaTransaccion(models.Model):
    _name = 'feria.linea_transaccion'
    _description = 'Línea de transacción'
    _rec_name = 'iNumeroLinea'
    _rec_names_search = ['transaccion_id', 'iNumeroLinea']
    _sql_constraints = [
        ('numero_linea_uniq', 'UNIQUE ("transaccion_id", "iNumeroLinea")',
         'Ya existe una línea con ese número en esta transacción.'),
    ]

    iNumeroLinea = fields.Integer(string='Número de línea', required=True)
    iCantidad = fields.Integer(string='Cantidad', required=True)
    iCantidadRecibida = fields.Integer(string='Cantidad recibida')
    fPrecioUnitario = fields.Float(string='Precio unitario')

    transaccion_id = fields.Many2one('feria.transaccion', string='Transacción', required=True, ondelete='cascade')
    linea_pedido_id = fields.Many2one('feria.linea_transaccion', string='Línea de pedido', ondelete='set null')
    linea_factura_ids = fields.One2many('feria.linea_transaccion', 'linea_pedido_id', string='Líneas de factura')

    fSubtotal = fields.Float(string='Subtotal', compute='_compute_subtotal')
    iCantidadFacturada = fields.Integer(string='Cantidad facturada', compute='_compute_cantidad_facturada')

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
            if oRegistro.iCantidad > 1000000:
                raise ValidationError('«Cantidad» no puede superar 1.000.000 de unidades.')

    @api.constrains('iCantidadRecibida', 'iCantidad')
    def _check_cantidad_recibida(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.iCantidadRecibida < 0:
                raise ValidationError('«Cantidad recibida» no puede ser menor que 0.')
            if oRegistro.iCantidadRecibida > oRegistro.iCantidad:
                raise ValidationError('«Cantidad recibida» no puede superar «Cantidad».')

    @api.constrains('fPrecioUnitario')
    def _check_precio_unitario(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.fPrecioUnitario < 0:
                raise ValidationError('«Precio unitario» no puede ser menor que 0.')
            if oRegistro.fPrecioUnitario > 1000000:
                raise ValidationError('«Precio unitario» no puede superar 1.000.000 €.')
            if round(oRegistro.fPrecioUnitario, 2) != oRegistro.fImporte:
                raise ValidationError('«Precio unitario» solo admite dos decimales (céntimos).')


    @api.constrains('iCantidad', 'linea_pedido_id')
    def _check_cantidad_facturada(self):
        oRegistro = None
        oLinea = None
        for oRegistro in self:
            for oLinea in oRegistro | oRegistro.linea_pedido_id:
                if oLinea.iCantidadFacturada > oLinea.iCantidad:
                    raise ValidationError('La línea de pedido «%s» quedaría con %s unidades facturadas y solo tiene %s pedidas.' % (
                        oLinea.display_name,
                        oLinea.iCantidadFacturada,
                        oLinea.iCantidad,
                    ))
    @api.constrains('transaccion_id', 'iCantidadRecibida', 'linea_pedido_id')
    def _check_tipo_linea(self):
        oRegistro = None
        sTipo = ''
        for oRegistro in self:
            sTipo = oRegistro.transaccion_id.tipo_transaccion_id.sCodigo
            if sTipo not in ('PED', 'FAC', 'ABO'):
                raise ValidationError('Solo las transacciones PED, FAC o ABO pueden tener líneas (%s es %s).' % (
                    oRegistro.transaccion_id.sIdTransaccion,
                    sTipo,
                ))
            if oRegistro.iCantidadRecibida and sTipo != 'PED':
                raise ValidationError('La «Cantidad recibida» solo se puede indicar en líneas de un PED.')
            if oRegistro.linea_factura_ids and sTipo != 'PED':
                raise ValidationError('La línea %s tiene líneas de factura y solo se pueden facturar líneas de un PED.' % oRegistro.display_name)
            if oRegistro.linea_pedido_id:
                if sTipo not in ('FAC', 'ABO'):
                    raise ValidationError('Solo las líneas de una FAC o un ABO pueden facturar una línea de pedido.')
                if oRegistro.linea_pedido_id.transaccion_id.tipo_transaccion_id.sCodigo != 'PED':
                    raise ValidationError('La «Línea de pedido» elegida (%s) tiene que ser de un PED.' % oRegistro.linea_pedido_id.display_name)
                
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

    @api.depends('transaccion_id.sIdTransaccion', 'iNumeroLinea')
    def _compute_display_name(self):
        oRegistro = None
        for oRegistro in self:
            oRegistro.display_name = '%s / %s' % (oRegistro.transaccion_id.sIdTransaccion or '', oRegistro.iNumeroLinea)

    @api.depends('iCantidad', 'fPrecioUnitario')
    def _compute_subtotal(self):
        oRegistro = None
        for oRegistro in self:
            oRegistro.fSubtotal = oRegistro.iCantidad * oRegistro.fPrecioUnitario

    @api.depends('linea_factura_ids.iCantidad')
    def _compute_cantidad_facturada(self):
        oRegistro = None
        for oRegistro in self:
            oRegistro.iCantidadFacturada = sum(oRegistro.linea_factura_ids.mapped('iCantidad'))
