from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class Producto(models.Model):

    _name = 'upoferia.producto'
    _description = 'Producto de barra'
    _rec_name = 'sNombre'

    sCodigoInterno = fields.Char(string="Código interno", required=True, help="Identificador único del producto")
    sNombre = fields.Char(string="Nombre", required=True)
    sAlergenos = fields.Char(string="Alérgenos")
    fPrecioSocio = fields.Float(string="Precio socio", digits=(10, 2))
    iXpOtorgada = fields.Integer(string="XP otorgada", default=0)
    
    # Relaciones
    tipo_producto_id = fields.Many2one('upoferia.tipo_producto', string="Tipo de producto", required=True)
    linea_ticket_ids = fields.One2many('upoferia.linea_ticket', 'producto_id', string="Líneas de ticket")
    # Relaciones con modelos de otro grupo
    marca_id = fields.Many2one('upoferia.marca', string="Marca")  # MARCA (nombre_marca)
    linea_transaccion_ids = fields.One2many('upoferia.linea_transaccion', 'producto_id', string="Líneas de transacción")  # LINEA_TRANSACCION (codigo_interno_producto)

    _sql_constraints = [
        ('codigo_interno_unique', 'UNIQUE("sCodigoInterno")', 'Ya existe un producto con ese código interno.'),
    ]

    @api.constrains('sCodigoInterno')
    def _check_codigo_interno(self):
        for record in self:
            if not re.fullmatch(r'[A-Z0-9_-]+', record.sCodigoInterno or ''):
                raise ValidationError('El código interno «%s» solo puede contener letras mayúsculas, números, '
                                      'guiones y guiones bajos, sin espacios.' % record.sCodigoInterno)

    @api.constrains('sNombre')
    def _check_nombre(self):
        for record in self:
            if not record.sNombre.strip():
                raise ValidationError('El nombre del producto no puede estar vacío.')

    @api.constrains('fPrecioSocio')
    def _check_precio_socio(self):
        for record in self:
            if record.fPrecioSocio < 0:
                raise ValidationError('El precio de socio no puede ser negativo.')

    @api.constrains('iXpOtorgada')
    def _check_xp_otorgada(self):
        for record in self:
            if record.iXpOtorgada < 0:
                raise ValidationError('La experiencia otorgada no puede ser negativa.')

    @api.onchange('sCodigoInterno')
    def onchange_codigo_interno(self):
        if self.sCodigoInterno:
            self.sCodigoInterno = self.sCodigoInterno.strip().upper().replace(' ', '_')

    @api.onchange('fPrecioSocio')
    def onchange_precio_socio(self):
        if self.fPrecioSocio < 0:
            return {
                'value': {'fPrecioSocio': 0.0},
                'warning': {
                    'title': 'Precio incorrecto',
                    'message': 'El precio de socio no puede ser negativo.'
                }
            }

    @api.onchange('iXpOtorgada')
    def onchange_xp_otorgada(self):
        if self.iXpOtorgada < 0:
            return {
                'value': {'iXpOtorgada': 0},
                'warning': {
                    'title': 'Experiencia incorrecta',
                    'message': 'La experiencia otorgada no puede ser negativa.'
                }
            }
        if self.iXpOtorgada > 500:
            return {
                'warning': {
                    'title': 'Experiencia elevada',
                    'message': 'Este producto da %s puntos de experiencia por unidad. Comprueba que no es una errata.'
                               % self.iXpOtorgada
                }
            }