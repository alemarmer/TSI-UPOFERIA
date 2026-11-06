import re

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

    tipo_transaccion_id = fields.Many2one('feria.tipo_transaccion', string='Tipo de transacción', required=True, ondelete='restrict')
    proveedor_id = fields.Many2one('feria.proveedor', string='Proveedor', required=True, ondelete='restrict')
    transaccion_origen_id = fields.Many2one('feria.transaccion', string='Transacción de origen', ondelete='set null')
    transaccion_derivada_ids = fields.One2many('feria.transaccion', 'transaccion_origen_id', string='Transacciones generadas')
    linea_ids = fields.One2many('feria.linea_transaccion', 'transaccion_id', string='Líneas')

    fImporteFacturado = fields.Float(string='Importe facturado', compute='_compute_importe_facturado')
    sCodigoTipo = fields.Char(string='Código del tipo', related='tipo_transaccion_id.sCodigo')

    @api.constrains('sIdTransaccion')
    def _check_id_transaccion(self):
        oRegistro = None
        sId = ''
        for oRegistro in self:
            sId = oRegistro.sIdTransaccion or ''
            if not sId.strip():
                raise ValidationError('El campo «Id. transacción» es obligatorio.')
            if not 2 <= len(sId) <= 20:
                raise ValidationError('El «Id. transacción» debe tener entre 2 y 20 caracteres.')
            if not re.fullmatch(r'[A-Z0-9]+([-/._][A-Z0-9]+)*', sId):
                raise ValidationError('El «Id. transacción» solo puede tener letras mayúsculas y números, separados por - / . _ y sin espacios (por ejemplo PED-2026-001).')

    @api.constrains('fImporte')
    def _check_importe(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.fImporte < 0:
                raise ValidationError('«Importe» no puede ser menor que 0.')
            if oRegistro.fImporte > 10000000:
                raise ValidationError('«Importe» no puede superar los 10.000.000 €.')
            if round(oRegistro.fImporte, 2) != oRegistro.fImporte:
                raise ValidationError('«Importe» solo admite dos decimales (céntimos).')

    @api.constrains('dFechaInicial')
    def _check_fecha_inicial(self):
        oRegistro = None
        dHoy = fields.Date.context_today(self)
        dFechaMinima = fields.Date.to_date('1970-01-01')
        for oRegistro in self:
            if not oRegistro.dFechaInicial:
                continue
            if oRegistro.dFechaInicial < dFechaMinima:
                raise ValidationError('La «Fecha inicial» no puede ser anterior al 01/01/1970.')
            if (oRegistro.dFechaInicial - dHoy).days > 730:
                raise ValidationError('La «Fecha inicial» no puede ser más de dos años posterior a hoy.')

    @api.constrains('dFechaInicial', 'dVencimiento')
    def _check_vencimiento(self):
        oRegistro = None
        for oRegistro in self:
            if not oRegistro.dVencimiento:
                continue
            if not oRegistro.dFechaInicial:
                raise ValidationError('No se puede indicar el «Vencimiento» sin la «Fecha inicial».')
            if oRegistro.dVencimiento < oRegistro.dFechaInicial:
                raise ValidationError('«Vencimiento» no puede ser anterior a «Fecha inicial».')
            if (oRegistro.dVencimiento - oRegistro.dFechaInicial).days > 365:
                raise ValidationError('El «Vencimiento» no puede ser más de un año posterior a la «Fecha inicial».')

    @api.constrains('dFechaInicial', 'dFechaPrevistaFin')
    def _check_fecha_prevista_fin(self):
        oRegistro = None
        for oRegistro in self:
            if not oRegistro.dFechaPrevistaFin:
                continue
            if not oRegistro.dFechaInicial:
                raise ValidationError('No se puede indicar la «Fecha prevista de fin» sin la «Fecha inicial».')
            if oRegistro.dFechaPrevistaFin < oRegistro.dFechaInicial:
                raise ValidationError('«Fecha prevista de fin» no puede ser anterior a «Fecha inicial».')
            if (oRegistro.dFechaPrevistaFin - oRegistro.dFechaInicial).days > 10 * 365:
                raise ValidationError('La «Fecha prevista de fin» no puede ser más de diez años posterior a la «Fecha inicial».')

    @api.constrains('sDocumento')
    def _check_documento(self):
        oRegistro = None
        sDocumento = ''
        for oRegistro in self:
            sDocumento = oRegistro.sDocumento or ''
            if not sDocumento:
                continue
            if ' ' in sDocumento:
                raise ValidationError('El «Documento» es una URL o una ruta de archivo y no puede tener espacios.')
            if len(sDocumento) > 255:
                raise ValidationError('El «Documento» no puede tener más de 255 caracteres.')
            if not re.fullmatch(r'(?i)https?://\S+|\S+\.(pdf|docx?|odt)', sDocumento):
                raise ValidationError('El «Documento» debe ser una URL que empiece por http:// o https://, o un archivo .pdf, .doc, .docx u .odt.')

    @api.constrains('sRefProveedor')
    def _check_ref_proveedor(self):
        oRegistro = None
        sReferencia = ''
        for oRegistro in self:
            sReferencia = oRegistro.sRefProveedor or ''
            if not sReferencia:
                continue
            if sReferencia != sReferencia.strip() or '  ' in sReferencia:
                raise ValidationError('La «Referencia del proveedor» no puede empezar ni terminar con espacios ni tener dos espacios seguidos.')
            if len(sReferencia) > 30:
                raise ValidationError('La «Referencia del proveedor» no puede tener más de 30 caracteres.')
            if not re.fullmatch(r"[A-Za-z0-9 \-/._]+", sReferencia):
                raise ValidationError('La «Referencia del proveedor» solo puede tener letras, números, espacios y los signos - / . _ (por ejemplo F-2026/0001).')

    @api.constrains('sRefProveedor', 'proveedor_id', 'tipo_transaccion_id')
    def _check_ref_proveedor_unica(self):
        oRegistro = None
        oOtra = None
        for oRegistro in self:
            if not oRegistro.sRefProveedor:
                continue
            if oRegistro.tipo_transaccion_id.sCodigo not in ('FAC', 'ABO'):
                continue
            oOtra = self.search([
                ('id', '!=', oRegistro.id),
                ('proveedor_id', '=', oRegistro.proveedor_id.id),
                ('sRefProveedor', '=', oRegistro.sRefProveedor),
                ('tipo_transaccion_id.sCodigo', 'in', ('FAC', 'ABO')),
            ], limit=1)
            if oOtra:
                raise ValidationError('El proveedor ya tiene otra factura o abono con la referencia «%s» (%s).' % (
                    oRegistro.sRefProveedor,
                    oOtra.sIdTransaccion,
                ))
    @api.constrains('transaccion_origen_id', 'tipo_transaccion_id', 'proveedor_id')
    def _check_genera(self):
        oRegistro = None
        oTransaccion = None
        sOrigen = ''
        sDerivada = ''
        lParejas = [('CON', 'PED'), ('CON', 'FAC'), ('CON', 'ABO'), ('PED', 'ALB')]
        for oRegistro in self:
            for oTransaccion in oRegistro | oRegistro.transaccion_derivada_ids:
                if not oTransaccion.transaccion_origen_id:
                    continue
                sOrigen = oTransaccion.transaccion_origen_id.tipo_transaccion_id.sCodigo
                sDerivada = oTransaccion.tipo_transaccion_id.sCodigo
                if (sOrigen, sDerivada) not in lParejas:
                    raise ValidationError('Una transacción %s no puede generarse a partir de una %s (%s → %s). Solo se permite CON → PED, CON → FAC, CON → ABO y PED → ALB.' % (
                        sDerivada,
                        sOrigen,
                        oTransaccion.transaccion_origen_id.sIdTransaccion,
                        oTransaccion.sIdTransaccion,
                    ))
                if oTransaccion.proveedor_id != oTransaccion.transaccion_origen_id.proveedor_id:
                    raise ValidationError('La transacción %s y la transacción de origen %s tienen que ser del mismo proveedor.' % (
                        oTransaccion.sIdTransaccion,
                        oTransaccion.transaccion_origen_id.sIdTransaccion,
                    ))

    @api.constrains('tipo_transaccion_id', 'linea_ids')
    def _check_lineas(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.tipo_transaccion_id.sCodigo in ('PED', 'FAC', 'ABO') and not oRegistro.linea_ids:
                raise ValidationError('Una transacción PED, FAC o ABO tiene que tener como mínimo una línea.')
            oRegistro.linea_ids._check_tipo_linea()
    
    @api.constrains('tipo_transaccion_id', 'sEstado', 'fImporte', 'dVencimiento', 'dFechaPrevistaFin', 'bRenovacionAuto', 'sDocumento', 'sRefProveedor')
    def _check_segun_tipo(self):
        oRegistro = None
        sTipo = ''
        sCampo = ''
        sEtiqueta = ''
        tTipos = ()
        sTipoEstado = ''
        tEstados = ()
        lAtributos = [
            ('fImporte', 'Importe', ('PED', 'FAC', 'ABO', 'CON')),
            ('dVencimiento', 'Vencimiento', ('FAC', 'ABO')),
            ('dFechaPrevistaFin', 'Fecha prevista de fin', ('PED', 'ALB', 'CON')),
            ('bRenovacionAuto', 'Renovación automática', ('CON',)),
            ('sDocumento', 'Documento', ('CON',)),
            ('sRefProveedor', 'Referencia del proveedor', ('FAC', 'ABO')),
        ]
        lEstados = [
            ('PED', ('borrador', 'confirmado', 'recibido', 'cancelado')),
            ('ALB', ('previsto', 'hecho')),
            ('FAC', ('pendiente', 'pagada', 'vencida')),
            ('ABO', ('pendiente', 'pagada', 'vencida')),
            ('CON', ('borrador', 'vigente', 'vencido', 'rescindido')),
        ]
        for oRegistro in self:
            sTipo = oRegistro.tipo_transaccion_id.sCodigo
            for sCampo, sEtiqueta, tTipos in lAtributos:
                if oRegistro[sCampo] and sTipo not in tTipos:
                    raise ValidationError('El campo «%s» solo se puede rellenar en transacciones %s (esta es %s).' % (
                        sEtiqueta,
                        ', '.join(tTipos),
                        sTipo,
                    ))
            if not oRegistro.sEstado:
                raise ValidationError('El «Estado» es obligatorio.')
            for sTipoEstado, tEstados in lEstados:
                if sTipoEstado == sTipo and oRegistro.sEstado not in tEstados:
                    raise ValidationError('Una transacción %s solo puede estar en estado %s.' % (
                        sTipo,
                        ', '.join(tEstados),
                    ))
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

    @api.onchange('tipo_transaccion_id')
    def _onchange_tipo_transaccion(self):
        sTipo = self.tipo_transaccion_id.sCodigo
        if sTipo in ('PED', 'CON'):
            self.sEstado = 'borrador'
        elif sTipo == 'ALB':
            self.sEstado = 'previsto'
        elif sTipo in ('FAC', 'ABO'):
            self.sEstado = 'pendiente'

    @api.depends('transaccion_derivada_ids.fImporte', 'transaccion_derivada_ids.tipo_transaccion_id.sCodigo')
    def _compute_importe_facturado(self):
        oRegistro = None
        oFacturas = None
        for oRegistro in self:
            oFacturas = oRegistro.transaccion_derivada_ids.filtered(lambda oTransaccion: oTransaccion.tipo_transaccion_id.sCodigo == 'FAC')
            oRegistro.fImporteFacturado = sum(oFacturas.mapped('fImporte'))

    def _cambiar_estado(self, sEstadoNuevo):
        oRegistro = None
        sTipo = ''
        lRecorrido = [
            ('PED', 'borrador', 'confirmado'),
            ('PED', 'confirmado', 'recibido'),
            ('PED', 'borrador', 'cancelado'),
            ('PED', 'confirmado', 'cancelado'),
            ('ALB', 'previsto', 'hecho'),
            ('FAC', 'pendiente', 'pagada'),
            ('FAC', 'pendiente', 'vencida'),
            ('FAC', 'vencida', 'pagada'),
            ('ABO', 'pendiente', 'pagada'),
            ('ABO', 'pendiente', 'vencida'),
            ('ABO', 'vencida', 'pagada'),
            ('CON', 'borrador', 'vigente'),
            ('CON', 'vigente', 'vencido'),
            ('CON', 'vigente', 'rescindido'),
        ]
        for oRegistro in self:
            sTipo = oRegistro.tipo_transaccion_id.sCodigo
            if (sTipo, oRegistro.sEstado, sEstadoNuevo) not in lRecorrido:
                raise ValidationError('Una transacción %s no puede pasar del estado «%s» a «%s».' % (
                    sTipo,
                    oRegistro.sEstado or 'sin estado',
                    sEstadoNuevo,
                ))
            oRegistro.write({'sEstado': sEstadoNuevo})

    def action_confirmar(self):
        self._cambiar_estado('confirmado')

    def action_recibir(self):
        self._cambiar_estado('recibido')

    def action_cancelar(self):
        self._cambiar_estado('cancelado')

    def action_hacer(self):
        self._cambiar_estado('hecho')

    def action_pagar(self):
        self._cambiar_estado('pagada')

    def action_marcar_vencida(self):
        self._cambiar_estado('vencida')

    def action_activar(self):
        self._cambiar_estado('vigente')

    def action_marcar_vencido(self):
        self._cambiar_estado('vencido')

    def action_rescindir(self):
        self._cambiar_estado('rescindido')