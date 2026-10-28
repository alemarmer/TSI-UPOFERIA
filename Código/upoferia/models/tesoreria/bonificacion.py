from odoo import models, fields


class Bonificacion(models.Model):

    _name = 'upoferia.bonificacion'
    _description = 'Bonificación aplicable a cuotas'
    _rec_name = 'nombre'

    nombre = fields.Char(string="Nombre", required=True, help="Identificador único de la bonificación")
    porcentaje_descuento = fields.Float(string="Porcentaje de descuento", required=True, digits=(5, 2))