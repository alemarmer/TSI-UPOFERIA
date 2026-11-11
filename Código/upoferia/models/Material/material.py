# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Material(models.Model):

    _name = 'upoferia.material'
    _description = 'Material'
    _rec_name = 'sNombre'
    _order = 'sCodigoInterno'

    sCodigoInterno = fields.Char(string='Código interno', required=True, help='Identificador único del material')
    sNombre = fields.Char(string='Nombre', required=True)
    selTipoPropiedad = fields.Selection([('fijo', 'Fijo'),
                                         ('propio', 'Propio'),
                                         ('alquilado', 'Alquilado'),],
                                        'Tipo de propiedad', required=True, default='propio')
    iCantidadTotal = fields.Integer(string='Cantidad total', default=1)
    selEstadoConservacion = fields.Selection([('nuevo', 'Nuevo'),
                                              ('bueno', 'Bueno'),
                                              ('regular', 'Regular'),
                                              ('deteriorado', 'Deteriorado'),],
                                             'Estado de conservación', default='bueno')
    dFechaAdquisicion = fields.Date(string='Fecha de adquisición')
    sObservaciones = fields.Text(string='Observaciones')

    # Relaciones
    categoria_material_id = fields.Many2one('upoferia.categoria_material', string='Categoría', required=True)
    uso_material_ids = fields.One2many('upoferia.uso_material', 'material_id', string='Usos en tareas')
    prestamo_linea_ids = fields.One2many('upoferia.prestamo_linea', 'material_id', string='Préstamos')

    _sql_constraints = [
        ('codigo_interno_unique', 'UNIQUE("sCodigoInterno")', 'Ya existe un material con ese código interno.'),
    ]

    @api.depends('sCodigoInterno', 'sNombre')
    def _compute_display_name(self):
        for record in self:
            record.display_name = '[%s] %s' % (record.sCodigoInterno or '', record.sNombre or '')

    @api.constrains('sCodigoInterno', 'sNombre')
    def _check_codigo_nombre(self):
        for record in self:
            if not record.sCodigoInterno.strip():
                raise models.ValidationError('El código interno del material no puede estar vacío.')
            if not record.sNombre.strip():
                raise models.ValidationError('El nombre del material no puede estar vacío.')

    @api.constrains('iCantidadTotal')
    def _check_cantidad_total(self):
        for record in self:
            if record.iCantidadTotal < 0:
                raise models.ValidationError('La cantidad total no puede ser negativa.')

    @api.onchange('iCantidadTotal')
    def onchange_cantidad_total(self):
        if self.iCantidadTotal == 0:
            return {
                'warning': {
                    'title': 'Cantidad a cero',
                    'message': 'El material tiene una cantidad total de 0. Comprueba que es correcto.',
                }
            }
