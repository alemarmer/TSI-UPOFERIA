from odoo import models, fields, api
import re


class CuentaBancaria(models.Model):

    _name = 'upoferia.cuenta_bancaria'
    _description = 'Cuenta bancaria de la caseta'
    _rec_name = 'sIban'

    sIban = fields.Char(string="IBAN", required=True, size=34, help="Identificador único de la cuenta bancaria")
    sBanco = fields.Char(string="Banco", required=True)
    sTitular = fields.Char(string="Titular", required=True)
    bActiva = fields.Boolean(string="Activa", default=True)
    
    # Relaciones
    movimiento_ids = fields.One2many('upoferia.movimiento', 'cuenta_bancaria_id', string="Movimientos")

    _sql_constraints = [
        ('iban_unique', 'UNIQUE("sIban")', 'Ya existe una cuenta bancaria con ese IBAN.'),
    ]

    @staticmethod
    def _iban_valido(iban):
        """Comprueba el formato y el dígito de control (módulo 97) de un IBAN."""
        if not re.fullmatch(r'[A-Z]{2}\d{2}[A-Z0-9]{11,30}', iban):
            return False
        if iban.startswith('ES') and len(iban) != 24:
            return False
        reordenado = iban[4:] + iban[:4]
        numerico = ''.join(str(int(c, 36)) for c in reordenado)
        return int(numerico) % 97 == 1

    @api.constrains('sIban')
    def _check_iban(self):
        for record in self:
            iban = record.sIban.replace(' ', '').upper()
            if not self._iban_valido(iban):
                raise models.ValidationError('El IBAN «%s» no es válido. Revisa que esté completo y bien escrito.' % record.sIban)

    @api.constrains('sBanco', 'sTitular')
    def _check_textos(self):
        for record in self:
            if not record.sBanco.strip():
                raise models.ValidationError('El nombre del banco no puede estar vacío.')
            if not record.sTitular.strip():
                raise models.ValidationError('El titular de la cuenta no puede estar vacío.')

    @api.onchange('sIban')
    def onchange_iban(self):
        if self.sIban:
            self.sIban = self.sIban.replace(' ', '').upper()
            if not self._iban_valido(self.sIban):
                return {
                    'warning': {
                        'title': 'IBAN incorrecto',
                        'message': 'El IBAN no tiene un formato válido o su dígito de control no cuadra.'
                    }
                }

    @api.onchange('bActiva')
    def onchange_activa(self):
        if not self.bActiva:
            return {
                'warning': {
                    'title': 'Cuenta desactivada',
                    'message': 'La cuenta no podrá usarse en nuevos movimientos, pero se conservan los que ya tiene.'
                }
            }