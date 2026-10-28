from odoo import models, fields


class Caja(models.Model):

    _name = 'upoferia.caja'
    _description = 'Caja o punto de cobro'
    _rec_name = 'nombre'

    nombre = fields.Char(string="Nombre", required=True, help="Identificador único de la caja")
    ubicacion = fields.Char(string="Ubicación")
    activa = fields.Boolean(string="Activa", default=True)