from odoo import models, fields


class Producto(models.Model):

    _name = 'upoferia.producto'
    _description = 'Producto de barra'
    _rec_name = 'nombre'

    codigo_interno = fields.Char(string="Código interno", required=True, help="Identificador único del producto")
    nombre = fields.Char(string="Nombre", required=True)
    alergenos = fields.Char(string="Alérgenos")
    precio_socio = fields.Float(string="Precio socio", digits=(10, 2))
    xp_otorgada = fields.Integer(string="XP otorgada", default=0)