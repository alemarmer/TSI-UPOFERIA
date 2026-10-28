from odoo import models, fields


class MetodoPago(models.Model):

    _name = 'upoferia.metodo_pago'
    _description = 'Método de pago'
    _rec_name = 'nombre'

    nombre = fields.Char(string="Nombre", required=True, help="Identificador único del método de pago")
    comision_porcentaje = fields.Float(string="Comisión (%)", digits=(5, 2), default=0.0)
    activo = fields.Boolean(string="Activo", default=True)