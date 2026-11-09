# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Transaccion(models.Model):
     _name = 'upoferia.transaccion'
     _description = 'Transacción con proveedor'
     _rec_name = 'sIdTransaccion'

     sIdTransaccion = fields.Char(string="Id. transacción", required=True)
     fImporte = fields.Float(string="Importe")
     sEstado = fields.Selection([('borrador', 'Borrador'),
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
                                 ('rescindido', 'Rescindido'),],
                                 'Estado', required=True)
     dFechaInicial = fields.Date(string="Fecha inicial")
     dVencimiento = fields.Date(string="Vencimiento")
     dFechaPrevistaFin = fields.Date(string="Fecha prevista de fin")
     bRenovacionAuto = fields.Boolean(string="Renovación automática")
     sDocumento = fields.Char(string="Documento")
     sRefProveedor = fields.Char(string="Referencia del proveedor")

     
     tipo_transaccion_id = fields.Many2one("upoferia.tipo_transaccion", string="Tipo de transacción", required=True)
     proveedor_id = fields.Many2one("upoferia.proveedor", string="Proveedor", required=True)
     transaccion_origen_id = fields.Many2one("upoferia.transaccion", string="Transacción de origen")
     transaccion_derivada_ids = fields.One2many("upoferia.transaccion", 'transaccion_origen_id', string="Transacciones generadas")
     linea_ids = fields.One2many("upoferia.linea_transaccion", 'transaccion_id', string="Líneas")
     linea_presupuesto_id = fields.Many2one("upoferia.linea_presupuesto", string="Línea de presupuesto")
     movimiento_ids = fields.One2many("upoferia.movimiento", 'transaccion_id', string="Movimientos")
     actuacion_ids = fields.One2many("upoferia.actuacion", 'transaccion_id', string="Actuaciones")
     salida_ids = fields.One2many("upoferia.salida", 'transaccion_id', string="Salidas")
     caseta_id = fields.Many2one("upoferia.caseta", string="Caseta")
     prestamo_ids = fields.One2many("upoferia.prestamo", 'transaccion_id', string="Préstamos")
     mantenimiento_ids = fields.One2many("upoferia.mantenimiento", 'transaccion_id', string="Mantenimientos")
     fImporteFacturado = fields.Float(compute='_importeFacturado', string="Importe facturado")
     sCodigoTipo = fields.Char(related='tipo_transaccion_id.sCodigo', string="Código del tipo")


     _sql_constraints = [('transaccion_id_unique', 'UNIQUE ("sIdTransaccion")', 'Ya existe una transacción con ese identificador')]

     def btn_eliminarLineas(self):
          for linea in self.linea_ids:
               self.write({'linea_ids':[(2,linea.id)]})   
                
     def btn_confirmar(self):
          self.write({'sEstado': 'confirmado'})

     def btn_recibir(self):
          self.write({'sEstado': 'recibido'})

     def btn_cancelar(self):
          self.write({'sEstado': 'cancelado'})

     def btn_hacer(self):
          self.write({'sEstado': 'hecho'})

     def btn_pagar(self):
          self.write({'sEstado': 'pagada'})

     def btn_marcar_vencida(self):
          self.write({'sEstado': 'vencida'})

     def btn_activar(self):
          self.write({'sEstado': 'vigente'})

     def btn_marcar_vencido(self):
          self.write({'sEstado': 'vencido'})

     def btn_rescindir(self):
          self.write({'sEstado': 'rescindido'})

     @api.depends('transaccion_derivada_ids.fImporte', 'transaccion_derivada_ids.tipo_transaccion_id.sCodigo')
     def _importeFacturado(self):
          for record in self:
               facturas = record.transaccion_derivada_ids.filtered(lambda transaccion: transaccion.tipo_transaccion_id.sCodigo == 'FAC')
               record.fImporteFacturado = sum(facturas.mapped('fImporte'))

     @api.constrains('fImporte')
     def _check_importe(self):
          for record in self:
               if record.fImporte < 0:
                    raise models.ValidationError('El importe no puede ser menor que 0.')

     @api.constrains('dFechaInicial', 'dVencimiento', 'dFechaPrevistaFin')
     def _check_fechas(self):
          for record in self:
               if record.dFechaInicial and record.dVencimiento and record.dVencimiento < record.dFechaInicial:
                    raise models.ValidationError('El vencimiento no puede ser anterior a la fecha inicial.')
               if record.dFechaInicial and record.dFechaPrevistaFin and record.dFechaPrevistaFin < record.dFechaInicial:
                    raise models.ValidationError('La fecha prevista de fin no puede ser anterior a la fecha inicial.')

     @api.constrains('tipo_transaccion_id', 'sEstado')
     def _check_estado(self):
          for record in self:
               tipo = record.tipo_transaccion_id.sCodigo
               if tipo == 'PED':
                    estados = ('borrador', 'confirmado', 'recibido', 'cancelado')
               elif tipo == 'ALB':
                    estados = ('previsto', 'hecho')
               elif tipo in ('FAC', 'ABO'):
                    estados = ('pendiente', 'pagada', 'vencida')
               else:
                    estados = ('borrador', 'vigente', 'vencido', 'rescindido')
               if record.sEstado not in estados:
                    raise models.ValidationError('Una transacción %s solo puede estar en estado %s.' % (tipo, ', '.join(estados)))

     @api.constrains('sIdTransaccion')
     def _check_IdTransaccion(self):
          for record in self:
               if ' ' in record.sIdTransaccion or record.sIdTransaccion != record.sIdTransaccion.upper():
                    raise models.ValidationError('El id debe ir en mayúsculas y sin espacios.')

     @api.onchange('tipo_transaccion_id')
     def onchange_tipo_transaccion(self):
          tipo = self.tipo_transaccion_id.sCodigo
          if tipo in ('PED', 'CON'):
               self.sEstado = 'borrador'
          elif tipo == 'ALB':
               self.sEstado = 'previsto'
          elif tipo in ('FAC', 'ABO'):
               self.sEstado = 'pendiente'
