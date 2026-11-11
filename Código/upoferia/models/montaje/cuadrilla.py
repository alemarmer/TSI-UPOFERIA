# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Cuadrilla(models.Model):

    _name = 'upoferia.cuadrilla'
    _description = 'Cuadrilla de montaje'
    _rec_name = 'sNombre'

    sNombre = fields.Char(string='Nombre', required=True, help='Identificador único de la cuadrilla')
    sEspecialidad = fields.Char(string='Especialidad')
    bActiva = fields.Boolean(string='Activa', default=True)

    # Relaciones
    # PENDIENTE DE INTEGRAR CON RRHH (necesita upoferia.empleado):
    # cuadrilla_empleado_ids = fields.One2many('upoferia.cuadrilla_empleado', 'cuadrilla_id', string='Miembros')
    tarea_montaje_ids = fields.One2many('upoferia.tarea_montaje', 'cuadrilla_id', string='Tareas de montaje')

    _sql_constraints = [
        ('nombre_unique', 'UNIQUE("sNombre")', 'Ya existe una cuadrilla con ese nombre.'),
    ]

    @api.constrains('sNombre')
    def _check_nombre(self):
        for record in self:
            if not record.sNombre.strip():
                raise models.ValidationError('El nombre de la cuadrilla no puede estar vacío.')
