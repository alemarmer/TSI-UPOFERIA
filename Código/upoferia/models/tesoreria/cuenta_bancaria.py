from odoo import models, fields


class CuentaBancaria(models.Model):

    _name = 'upoferia.cuenta_bancaria'
    _description = 'Cuenta bancaria de la caseta'
    _rec_name = 'iban'

    iban = fields.Char(string="IBAN", required=True, size=34, help="Identificador único de la cuenta bancaria")
    banco = fields.Char(string="Banco", required=True)
    titular = fields.Char(string="Titular", required=True)
    activa = fields.Boolean(string="Activa", default=True)