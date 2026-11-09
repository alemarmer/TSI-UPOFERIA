# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class InspeccionInspector(models.Model):
    _name = 'feria.inspeccion_inspector'
    _description = 'Inspector de una inspección'
    _rec_name = 'inspector_id'
    _sql_constraints = [
        ('inspeccion_inspector_uniq', 'UNIQUE (inspeccion_id, inspector_id)',
         'Ese inspector ya está asignado a esta inspección.'),
    ]

    sRol = fields.Char(string='Rol')

    inspeccion_id = fields.Many2one('feria.inspeccion', string='Inspección', required=True, ondelete='cascade')
    inspector_id = fields.Many2one('feria.inspector', string='Inspector', required=True, ondelete='cascade')

    @api.constrains('sRol')
    def _check_rol(self):
        oRegistro = None
        sRol = ''
        for oRegistro in self:
            sRol = oRegistro.sRol or ''
            if not sRol:
                continue
            if not sRol.strip():
                raise ValidationError('El campo «Rol» no puede estar formado solo por espacios.')
            if sRol != sRol.strip():
                raise ValidationError('El «Rol» del inspector no puede empezar ni terminar con espacios.')
            if not 2 <= len(sRol) <= 100:
                raise ValidationError('El «Rol» del inspector debe tener entre 2 y 100 caracteres.')
