# -*- coding: utf-8 -*-
# Tabla PROVEEDOR del modelo relacional · bloque PROVEEDORES Y CONTRATOS
# Subtipo de PERSONA: su clave (dni) es la del supertipo
# y se resolverá con herencia en la fase de relaciones.
# Validaciones de atributo: implementadas al final de la clase.

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

    # Único; solo se rellena si el proveedor es una empresa (E-R)
    sCif = fields.Char(string='CIF')

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
