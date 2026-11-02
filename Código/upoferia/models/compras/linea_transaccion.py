# -*- coding: utf-8 -*-
# Tabla LINEA_TRANSACCION del modelo relacional · bloque COMPRAS A PROVEEDORES
# Entidad débil: su clave incluye la clave ajena (id_transaccion), que se añade en la fase de relaciones.
# Validaciones de atributo: implementadas al final de la clase.
#
# Pendiente para la fase de relaciones (no incluido aquí):
#   Claves ajenas:
#     - id_transaccion -> TRANSACCION (obligatoria, parte de la clave)
#     - id_transaccion_pedido, numero_linea_pedido -> LINEA_TRANSACCION (opcional)
#     - codigo_interno_producto -> PRODUCTO (opcional)
#   Atributos derivados (campos compute):
#     - subtotal = cantidad x precio_unitario
#     - cantidad_facturada (solo líneas de PED)
#   Validaciones que necesitan claves ajenas:
#     - cantidad_facturada <= cantidad (cuando exista el campo derivado)
#     - UNIQUE(id_transaccion, numero_linea) cuando exista la FK

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LineaTransaccion(models.Model):
    _name = 'feria.linea_transaccion'
    _description = 'Línea de transacción'
    _rec_name = 'numero_linea'

    # Discriminante: la clave completa es (id_transaccion, numero_linea)
    numero_linea = fields.Integer(string='Número de línea', required=True)
    cantidad = fields.Integer(string='Cantidad')
    # Solo en líneas de PED
    cantidad_recibida = fields.Integer(string='Cantidad recibida')
    precio_unitario = fields.Float(string='Precio unitario')

    # «Número de línea» debe ser mayor que 0 (básica)
    @api.constrains('numero_linea')
    def _check_numero_linea(self):
        for record in self:
            if record.numero_linea <= 0:
                raise ValidationError('«Número de línea» debe ser mayor que 0.')

    # «Cantidad» debe ser mayor que 0 (básica)
    @api.constrains('cantidad')
    def _check_cantidad(self):
        for record in self:
            if record.cantidad <= 0:
                raise ValidationError('«Cantidad» debe ser mayor que 0.')

    # «Cantidad recibida» no puede ser menor que 0 (básica)
    @api.constrains('cantidad_recibida')
    def _check_cantidad_recibida(self):
        for record in self:
            if record.cantidad_recibida < 0:
                raise ValidationError('«Cantidad recibida» no puede ser menor que 0.')

    # «Cantidad recibida» no puede superar «Cantidad» (E-R)
    @api.constrains('cantidad_recibida', 'cantidad')
    def _check_cantidad_recibida_cantidad(self):
        for record in self:
            if record.cantidad_recibida > record.cantidad:
                raise ValidationError('«Cantidad recibida» no puede superar «Cantidad».')

    # «Precio unitario» no puede ser menor que 0 (básica)
    @api.constrains('precio_unitario')
    def _check_precio_unitario(self):
        for record in self:
            if record.precio_unitario < 0:
                raise ValidationError('«Precio unitario» no puede ser menor que 0.')

    # Aviso inmediato en el formulario, antes de guardar (como el onchange de gym_2)
    @api.onchange('cantidad_recibida', 'cantidad')
    def _onchange_valores(self):
        mensaje = False
        if self.cantidad_recibida > self.cantidad:
            mensaje = '«Cantidad recibida» no puede superar «Cantidad».'
        if mensaje:
            return {
                'warning': {
                    'title': 'Valores incorrectos',
                    'message': mensaje,
                }
            }
