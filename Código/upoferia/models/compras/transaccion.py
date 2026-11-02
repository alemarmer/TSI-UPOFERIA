# -*- coding: utf-8 -*-
# Tabla TRANSACCION del modelo relacional · bloque COMPRAS A PROVEEDORES
# Validaciones de atributo: implementadas al final de la clase.
#
# Pendiente para la fase de relaciones (no incluido aquí):
#   Claves ajenas:
#     - codigo_tipo_transaccion -> TIPO_TRANSACCION (obligatoria)
#     - id_transaccion_origen -> TRANSACCION (opcional)
#     - dni_proveedor -> PROVEEDOR (obligatoria)
#     - nombre_caseta -> CASETA (opcional)
#     - ejercicio_presupuesto, concepto_linea_presupuesto -> LINEA_PRESUPUESTO (opcional)
#   Atributos derivados (campos compute):
#     - importe_facturado (CON) = suma de los importes de las FAC que genera
#   Validaciones que necesitan claves ajenas:
#     - Cada tipo solo admite sus atributos y sus estados (necesita la FK al tipo)
#     - PROVEEDOR + ref_proveedor no se repite en FAC/ABO (necesita la FK al proveedor)
#     - importe de FAC/ABO = suma de los subtotales de sus líneas (necesita las líneas)

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Transaccion(models.Model):
    _name = 'feria.transaccion'
    _description = 'Transacción con proveedor'
    _rec_name = 'id_transaccion'
    _sql_constraints = [
        ('id_transaccion_uniq', 'UNIQUE (id_transaccion)',
         'Ya existe una transacción con ese identificador.'),
    ]

    # Clave artificial del E-R (Odoo crea además su propio id)
    id_transaccion = fields.Char(string='Id. transacción', required=True)
    # Solo PED, FAC/ABO y CON
    importe = fields.Float(string='Importe')
    # Unión de los estados que el E-R da para PED, ALB, FAC/ABO y CON
    estado = fields.Selection(
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
    fecha_inicial = fields.Date(string='Fecha inicial')
    # Solo FAC/ABO
    vencimiento = fields.Date(string='Vencimiento')
    # Solo PED, ALB y CON
    fecha_prevista_fin = fields.Date(string='Fecha prevista de fin')
    # Solo CON
    renovacion_auto = fields.Boolean(string='Renovación automática')
    # Solo CON. En el UML es String; si debe guardar el fichero, cambiar a fields.Binary
    documento = fields.Char(string='Documento')
    # Solo FAC/ABO
    ref_proveedor = fields.Char(string='Referencia del proveedor')

    # «Id. transacción» obligatorio: no vale texto vacío ni solo espacios (básica)
    @api.constrains('id_transaccion')
    def _check_id_transaccion_obligatorio(self):
        for record in self:
            if not (record.id_transaccion or '').strip():
                raise ValidationError('El campo «Id. transacción» es obligatorio.')

    # «Importe» no puede ser menor que 0 (básica)
    @api.constrains('importe')
    def _check_importe(self):
        for record in self:
            if record.importe < 0:
                raise ValidationError('«Importe» no puede ser menor que 0.')

    # «Vencimiento» no puede ser anterior a «Fecha inicial» (E-R)
    @api.constrains('fecha_inicial', 'vencimiento')
    def _check_vencimiento(self):
        for record in self:
            if record.fecha_inicial and record.vencimiento and record.vencimiento < record.fecha_inicial:
                raise ValidationError('«Vencimiento» no puede ser anterior a «Fecha inicial».')

    # «Fecha prevista de fin» no puede ser anterior a «Fecha inicial» (E-R)
    @api.constrains('fecha_inicial', 'fecha_prevista_fin')
    def _check_fecha_prevista_fin(self):
        for record in self:
            if record.fecha_inicial and record.fecha_prevista_fin and record.fecha_prevista_fin < record.fecha_inicial:
                raise ValidationError('«Fecha prevista de fin» no puede ser anterior a «Fecha inicial».')

    # Aviso inmediato en el formulario, antes de guardar (como el onchange de gym_2)
    @api.onchange('fecha_inicial', 'vencimiento', 'fecha_prevista_fin')
    def _onchange_valores(self):
        mensaje = False
        if self.fecha_inicial and self.vencimiento and self.vencimiento < self.fecha_inicial:
            mensaje = '«Vencimiento» no puede ser anterior a «Fecha inicial».'
        if not mensaje and self.fecha_inicial and self.fecha_prevista_fin and self.fecha_prevista_fin < self.fecha_inicial:
            mensaje = '«Fecha prevista de fin» no puede ser anterior a «Fecha inicial».'
        if mensaje:
            return {
                'warning': {
                    'title': 'Valores incorrectos',
                    'message': mensaje,
                }
            }
