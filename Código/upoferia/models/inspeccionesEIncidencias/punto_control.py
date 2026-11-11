# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PuntoControl(models.Model):
    _name = 'upoferia.punto_control'
    _description = 'Punto de control'
    _rec_name = 'iNumeroPunto'
    _rec_names_search = ['inspeccion_id.sReferencia', 'iNumeroPunto']
    _order = 'inspeccion_id, iNumeroPunto'
    _sql_constraints = [
        ('inspeccion_numero_punto_uniq', 'UNIQUE (inspeccion_id, "iNumeroPunto")',
         'Esa inspección ya tiene un punto de control con ese número.'),
    ]

    iNumeroPunto = fields.Integer(string='Número de punto', required=True)
    sDescripcion = fields.Char(string='Descripción', required=True)
    sResultado = fields.Selection([
        ('superado', 'Superado'),
        ('no_superado', 'No superado'),
        ('no_aplica', 'No aplica'),
    ], string='Resultado')
    sObservaciones = fields.Text(string='Observaciones')

    inspeccion_id = fields.Many2one('upoferia.inspeccion', string='Inspección', required=True)
    elemento_seguridad_id = fields.Many2one('upoferia.elemento_seguridad', string='Elemento de seguridad')
    incidencia_ids = fields.One2many('upoferia.incidencia', 'punto_control_id', string='Incidencias detectadas')

    @api.depends('iNumeroPunto', 'inspeccion_id.sReferencia')
    def _compute_display_name(self):
        oRegistro = None
        for oRegistro in self:
            oRegistro.display_name = f'{oRegistro.inspeccion_id.sReferencia or ""} / {oRegistro.iNumeroPunto}'

    @api.constrains('elemento_seguridad_id', 'inspeccion_id')
    def _check_elemento_seguridad(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.elemento_seguridad_id and oRegistro.elemento_seguridad_id.caseta_id != oRegistro.inspeccion_id.caseta_id:
                raise models.ValidationError('El punto de control solo puede revisar elementos de seguridad de la caseta inspeccionada.')
