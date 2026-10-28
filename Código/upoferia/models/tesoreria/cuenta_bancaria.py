from odoo import models, fields


class CuentaBancaria(models.Model):

    _name = 'upoferia.cuenta_bancaria'
    _description = 'Cuenta bancaria de la caseta'
    _rec_name = 'iban'

    iban = fields.Char(string="IBAN", required=True, size=34, help="Identificador único de la cuenta bancaria")
    banco = fields.Char(string="Banco", required=True)
    titular = fields.Char(string="Titular", required=True)
    activa = fields.Boolean(string="Activa", default=True)
    
    _sql_constraints = [
        ('iban_unique', 'UNIQUE(iban)', 'Ya existe una cuenta bancaria con ese IBAN.'),
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

    @api.constrains('iban')
    def _check_iban(self):
        for record in self:
            iban = record.iban.replace(' ', '').upper()
            if not self._iban_valido(iban):
                raise ValidationError('El IBAN «%s» no es válido. Revisa que esté completo y bien escrito.' % record.iban)

    @api.constrains('banco', 'titular')
    def _check_textos(self):
        for record in self:
            if not record.banco.strip():
                raise ValidationError('El nombre del banco no puede estar vacío.')
            if not record.titular.strip():
                raise ValidationError('El titular de la cuenta no puede estar vacío.')

    @api.onchange('iban')
    def onchange_iban(self):
        if self.iban:
            self.iban = self.iban.replace(' ', '').upper()
            if not self._iban_valido(self.iban):
                return {
                    'warning': {
                        'title': 'IBAN incorrecto',
                        'message': 'El IBAN no tiene un formato válido o su dígito de control no cuadra.'
                    }
                }

    @api.onchange('activa')
    def onchange_activa(self):
        if not self.activa:
            return {
                'warning': {
                    'title': 'Cuenta desactivada',
                    'message': 'La cuenta no podrá usarse en nuevos movimientos, pero se conservan los que ya tiene.'
                }
            }