# -*- coding: utf-8 -*-

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
