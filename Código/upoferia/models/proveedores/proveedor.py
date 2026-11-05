import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Proveedor(models.Model):
    _name = 'feria.proveedor'
    _description = 'Proveedor'
    _sql_constraints = [
        ('cif_uniq', 'UNIQUE ("sCif")',
         'Ya existe un proveedor con ese CIF.'),
    ]

    sCif = fields.Char(string='CIF')

    transaccion_ids = fields.One2many('feria.transaccion', 'proveedor_id', string='Transacciones')
    categoria_ids = fields.Many2many('feria.categoria_proveedor', 'feria_proveedor_categoria_rel', 'proveedor_id', 'categoria_proveedor_id', string='Categorías')

    @api.constrains('sCif')
    def _check_cif(self):
        oRegistro = None
        sCif = ''
        iSumaPares = 0
        iSumaImpares = 0
        iDoble = 0
        iPosicion = 0
        iControl = 0
        sControlNumero = ''
        sControlLetra = ''
        bValido = False
        for oRegistro in self:
            sCif = oRegistro.sCif or ''
            if not sCif:
                continue
            if not re.fullmatch(r'[ABCDEFGHJNPQRSUVW][0-9]{7}[0-9A-J]', sCif):
                raise ValidationError('El CIF debe tener una letra mayúscula, 7 dígitos y un carácter de control, sin espacios (por ejemplo B12345674).')
            
            #a partir de aquí es la forma de validar el algoritmo matemático oficial de la Agencia Tributaria, que comprueba automaticamente con el digito de control haber si te has inventado o escrito mal algun numero
            iSumaPares = 0
            iSumaImpares = 0
            for iPosicion in range(1, 8):
                if iPosicion % 2 == 0:
                    iSumaPares += int(sCif[iPosicion])
                else:
                    iDoble = int(sCif[iPosicion]) * 2
                    iSumaImpares += iDoble // 10 + iDoble % 10
            iControl = (10 - (iSumaPares + iSumaImpares) % 10) % 10
            sControlNumero = str(iControl)
            sControlLetra = 'JABCDEFGHI'[iControl]
            if sCif[0] in 'PQRSNW':
                bValido = sCif[8] == sControlLetra
            elif sCif[0] in 'ABEH':
                bValido = sCif[8] == sControlNumero
            else:
                bValido = sCif[8] in (sControlNumero, sControlLetra)
            if not bValido:
                raise ValidationError('El carácter de control del CIF %s no es correcto.' % sCif)
