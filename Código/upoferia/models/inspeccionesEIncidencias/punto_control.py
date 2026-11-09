# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PuntoControl(models.Model):
    _name = 'feria.punto_control'
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

    inspeccion_id = fields.Many2one('feria.inspeccion', string='Inspección', required=True, ondelete='cascade')
    elemento_seguridad_id = fields.Many2one('feria.elemento_seguridad', string='Elemento de seguridad', ondelete='set null')
    incidencia_ids = fields.One2many('feria.incidencia', 'punto_control_id', string='Incidencias detectadas')

    @api.depends('iNumeroPunto', 'inspeccion_id.sReferencia')
    def _compute_display_name(self):
        oRegistro = None
        for oRegistro in self:
            oRegistro.display_name = f'{oRegistro.inspeccion_id.sReferencia or ""} / {oRegistro.iNumeroPunto}'

    @api.constrains('iNumeroPunto')
    def _check_numero_punto(self):
        oRegistro = None
        for oRegistro in self:
            if not 1 <= oRegistro.iNumeroPunto <= 999:
                raise ValidationError('El «Número de punto» debe estar entre 1 y 999.')

    @api.constrains('sDescripcion')
    def _check_descripcion(self):
        oRegistro = None
        sDescripcion = ''
        for oRegistro in self:
            sDescripcion = oRegistro.sDescripcion or ''
            if not sDescripcion.strip():
                raise ValidationError('El campo «Descripción» es obligatorio.')
            if sDescripcion != sDescripcion.strip():
                raise ValidationError('La «Descripción» del punto de control no puede empezar ni terminar con espacios.')
            if not 2 <= len(sDescripcion) <= 255:
                raise ValidationError('La «Descripción» del punto de control debe tener entre 2 y 255 caracteres.')

    @api.constrains('sObservaciones', 'sResultado')
    def _check_observaciones(self):
        oRegistro = None
        sObservaciones = ''
        for oRegistro in self:
            sObservaciones = oRegistro.sObservaciones or ''
            if oRegistro.sResultado == 'no_superado' and not sObservaciones.strip():
                raise ValidationError('Un punto de control no superado tiene que explicar el motivo en «Observaciones».')
            if not sObservaciones:
                continue
            if sObservaciones != sObservaciones.strip():
                raise ValidationError('Las «Observaciones» no pueden empezar ni terminar con espacios.')
            if len(sObservaciones) > 2000:
                raise ValidationError('Las «Observaciones» pueden tener como mucho 2.000 caracteres.')

    @api.constrains('sResultado', 'inspeccion_id')
    def _check_resultado(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.sResultado and oRegistro.inspeccion_id.sEstado != 'realizada':
                raise ValidationError('Solo se puede indicar el «Resultado» de un punto de control si la inspección está realizada.')

    @api.constrains('elemento_seguridad_id', 'inspeccion_id')
    def _check_elemento_seguridad(self):
        oRegistro = None
        for oRegistro in self:
            if not oRegistro.elemento_seguridad_id:
                continue
            if oRegistro.elemento_seguridad_id.caseta_id != oRegistro.inspeccion_id.caseta_id:
                raise ValidationError('El punto de control solo puede revisar elementos de seguridad de la caseta inspeccionada.')
