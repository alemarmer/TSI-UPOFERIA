# -*- coding: utf-8 -*-

import re

from odoo import models, fields, api


class Inspector(models.Model):
    _name = 'upoferia.inspector'
    _description = 'Inspector'
    _rec_name = 'sNumeroAcreditacion'
    _sql_constraints = [
        ('numero_acreditacion_uniq', 'UNIQUE ("sNumeroAcreditacion")',
         'Ya existe un inspector con ese número de acreditación.'),
    ]

    sNumeroAcreditacion = fields.Char(string='Número de acreditación', required=True)
    sOrganismo = fields.Char(string='Organismo')
    sCargo = fields.Char(string='Cargo')

    inspeccion_inspector_ids = fields.One2many('upoferia.inspeccion_inspector', 'inspector_id', string='Inspecciones')

    @api.constrains('sNumeroAcreditacion')
    def _check_numero_acreditacion(self):
        oRegistro = None
        sNumeroAcreditacion = ''
        for oRegistro in self:
            sNumeroAcreditacion = oRegistro.sNumeroAcreditacion or ''
            if not sNumeroAcreditacion.strip():
                raise models.ValidationError('El campo «Número de acreditación» es obligatorio.')
            if not 2 <= len(sNumeroAcreditacion) <= 20:
                raise models.ValidationError('El «Número de acreditación» debe tener entre 2 y 20 caracteres.')
            if not re.fullmatch(r'[A-Z0-9]+([-/._][A-Z0-9]+)*', sNumeroAcreditacion):
                raise models.ValidationError('El «Número de acreditación» solo puede tener letras mayúsculas y números, separados por - / . _ y sin espacios (por ejemplo ACR-SEV-0042).')

    @api.constrains('sOrganismo')
    def _check_organismo(self):
        oRegistro = None
        sOrganismo = ''
        for oRegistro in self:
            sOrganismo = oRegistro.sOrganismo or ''
            if not sOrganismo:
                continue
            if not sOrganismo.strip():
                raise models.ValidationError('El campo «Organismo» no puede estar formado solo por espacios.')
            if sOrganismo != sOrganismo.strip():
                raise models.ValidationError('El «Organismo» no puede empezar ni terminar con espacios.')
            if not 2 <= len(sOrganismo) <= 100:
                raise models.ValidationError('El «Organismo» debe tener entre 2 y 100 caracteres.')

    @api.constrains('sCargo')
    def _check_cargo(self):
        oRegistro = None
        sCargo = ''
        for oRegistro in self:
            sCargo = oRegistro.sCargo or ''
            if not sCargo:
                continue
            if not sCargo.strip():
                raise models.ValidationError('El campo «Cargo» no puede estar formado solo por espacios.')
            if sCargo != sCargo.strip():
                raise models.ValidationError('El «Cargo» no puede empezar ni terminar con espacios.')
            if not 2 <= len(sCargo) <= 100:
                raise models.ValidationError('El «Cargo» debe tener entre 2 y 100 caracteres.')


    def unlink(self):
        self.inspeccion_inspector_ids.unlink()
        return super().unlink()