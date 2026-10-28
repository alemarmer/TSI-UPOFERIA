from odoo import models, fields


class Tarifa(models.Model):

    _name = 'upoferia.tarifa'
    _description = 'Tarifa de precios'
    _rec_name = 'nombre'

    nombre = fields.Char(string="Nombre", required=True, help="Identificador único de la tarifa")
    moneda = fields.Char(string="Moneda", size=3, default='EUR', help="Código ISO de la moneda (EUR, USD…)")