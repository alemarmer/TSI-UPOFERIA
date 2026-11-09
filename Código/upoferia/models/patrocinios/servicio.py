# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Servicio(models.Model):
     _name = 'upoferia.servicio'
     _description = 'Servicio'
     _rec_name = 'sCodigo'

     sCodigo = fields.Char(string="Código", required=True)
     sNombre = fields.Char(string="Nombre", required=True)
     sUnidadFacturacion = fields.Selection([('hora', 'Por hora'),
                                            ('dia', 'Por día'),
                                            ('evento', 'Por evento'),
                                            ('unidad', 'Por unidad'),
                                            ('persona', 'Por persona'),
                                            ('metro_cuadrado', 'Por metro cuadrado'),
                                            ('precio_cerrado', 'Precio cerrado'),],
                                            'Unidad de facturación')
     bRequiereTecnico = fields.Boolean(string="Requiere técnico")

     
     servicio_proveedor_ids = fields.One2many("upoferia.servicio_proveedor", 'servicio_id', string="Proveedores que lo ofrecen")
     actuacion_ids = fields.Many2many("upoferia.actuacion", 'upoferia_actuacion_servicio', 'servicio_id', 'actuacion_id', string="Actuaciones")
     incidencia_ids = fields.One2many("upoferia.incidencia", 'servicio_id', string="Incidencias")
     
     _sql_constraints = [('servicio_codigo_unique', 'UNIQUE ("sCodigo")', 'Ya existe un servicio con ese código')]


     def btn_eliminarTarifas(self):
          for tarifa in self.servicio_proveedor_ids:
               self.write({'servicio_proveedor_ids':[(2,tarifa.id)]})