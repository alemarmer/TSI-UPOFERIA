# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta

class TareaMontaje(models.Model):

    _name = 'upoferia.tarea_montaje'
    _description = 'Tarea de montaje'
    _rec_name = 'sNombre'

    sNombre = fields.Char(string='Nombre', required=True, help='Identifica la tarea dentro de su fase')
    dFechaInicio = fields.Date(string='Fecha de inicio')
    dFechaLimite = fields.Date(string='Fecha límite')
    fHorasPrevistas = fields.Float(string='Horas previstas')
    selPrioridad = fields.Selection([('baja', 'Baja'),
                                     ('media', 'Media'),
                                     ('alta', 'Alta'),],
                                    'Prioridad', default='media')
    selEstado = fields.Selection([('pendiente', 'Pendiente'),
                                  ('en_curso', 'En curso'),
                                  ('hecha', 'Hecha'),],
                                 'Estado', default='pendiente')

    # Relaciones
    fase_montaje_id = fields.Many2one('upoferia.fase_montaje', string='Fase', required=True)
    # el plan se obtiene a través de la fase (cadena Plan -> Fase -> Tarea)
    plan_montaje_id = fields.Many2one(related='fase_montaje_id.plan_montaje_id', string='Plan de montaje', store=True)
    cuadrilla_id = fields.Many2one('upoferia.cuadrilla', string='Cuadrilla')
    transporte_ids = fields.One2many('upoferia.transporte', 'tarea_montaje_id', string='Transportes')
    uso_material_ids = fields.One2many('upoferia.uso_material', 'tarea_montaje_id', string='Material utilizado')

    _sql_constraints = [
        ('nombre_fase_unique', 'UNIQUE(fase_montaje_id, "sNombre")', 'Ya existe una tarea con ese nombre en esta fase.'),
    ]

    @api.constrains('sNombre')
    def _check_nombre(self):
        for record in self:
            if not record.sNombre.strip():
                raise models.ValidationError('El nombre de la tarea no puede estar vacío.')

    @api.constrains('fHorasPrevistas', 'dFechaInicio', 'dFechaLimite')
    def _check_horas_fechas(self):
        for record in self:
            if record.fHorasPrevistas < 0:
                raise models.ValidationError('Las horas previstas no pueden ser negativas.')
            if record.dFechaInicio and record.dFechaLimite and record.dFechaLimite < record.dFechaInicio:
                raise models.ValidationError('La fecha límite no puede ser anterior a la de inicio.')

    @api.onchange('dFechaInicio')
    def onchange_fecha_inicio(self):
        if self.dFechaInicio and not self.dFechaLimite:
            self.dFechaLimite = self.dFechaInicio + timedelta(days=1)

    def btn_submit_to_pendiente(self):
        self.write({'selEstado': 'pendiente'})

    def btn_submit_to_en_curso(self):
        self.write({'selEstado': 'en_curso'})

    def btn_submit_to_hecha(self):
        self.write({'selEstado': 'hecha'})
