# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Inspector(models.Model):
    _name = 'upoferia.inspector'
    _description = 'Inspector'
    _rec_name = 'sNumeroAcreditacion'
    _inherits = {'upoferia.socios.persona': 'persona_id'}

    sNumeroAcreditacion = fields.Char(string='Número de acreditación', required=True)
    sOrganismo = fields.Char(string='Organismo')
    sCargo = fields.Char(string='Cargo')

    inspeccion_inspector_ids = fields.One2many('upoferia.inspeccion_inspector', 'inspector_id', string='Inspecciones')
    persona_id = fields.Many2one('upoferia.socios.persona', string='Persona', required=True)

    _sql_constraints = [
            ('numero_acreditacion_uniq', 'UNIQUE ("sNumeroAcreditacion")',
             'Ya existe un inspector con ese número de acreditación.'),
    ]

    def unlink(self):
        self.inspeccion_inspector_ids.unlink()
        return super().unlink()
