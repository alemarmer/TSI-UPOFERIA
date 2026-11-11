# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InspeccionInspector(models.Model):
    _name = 'upoferia.inspeccion_inspector'
    _description = 'Inspector de una inspección'
    _rec_name = 'inspector_id'
    _sql_constraints = [
        ('inspeccion_inspector_uniq', 'UNIQUE (inspeccion_id, inspector_id)',
         'Ese inspector ya está asignado a esta inspección.'),
    ]

    sRol = fields.Char(string='Rol')

    inspeccion_id = fields.Many2one('upoferia.inspeccion', string='Inspección', required=True)
    inspector_id = fields.Many2one('upoferia.inspector', string='Inspector', required=True)
