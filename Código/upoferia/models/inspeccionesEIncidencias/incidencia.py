# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Incidencia(models.Model):
    _name = 'upoferia.incidencia'
    _description = 'Incidencia'
    _rec_name = 'sReferencia'
    _sql_constraints = [
        ('referencia_uniq', 'UNIQUE ("sReferencia")',
         'Ya existe una incidencia con esa referencia.'),
    ]

    sReferencia = fields.Char(string='Referencia', required=True)
    dFecha = fields.Date(string='Fecha', required=True, default=fields.Date.context_today)
    sPrioridad = fields.Selection([
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ], string='Prioridad', required=True, default='media')
    sEstado = fields.Selection([
        ('abierta', 'Abierta'),
        ('en_curso', 'En curso'),
        ('resuelta', 'Resuelta'),
        ('cancelada', 'Cancelada'),
    ], string='Estado', required=True, default='abierta')

    mobiliario_id = fields.Many2one('upoferia.mobiliario_caseta', string='Mobiliario afectado')
    punto_control_id = fields.Many2one('upoferia.punto_control', string='Punto de control que la detecta')
    mantenimiento_ids = fields.One2many('upoferia.mantenimiento', 'incidencia_id', string='Mantenimientos')

    @api.constrains('punto_control_id', 'mobiliario_id')
    def _check_punto_control(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.punto_control_id and oRegistro.mobiliario_id and oRegistro.mobiliario_id.caseta_id != oRegistro.punto_control_id.inspeccion_id.caseta_id:
                raise models.ValidationError('Si la incidencia la detecta un punto de control, el mobiliario afectado tiene que ser de la caseta inspeccionada.')

    def unlink(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.mantenimiento_ids:
                raise models.UserError(f'No se puede borrar la incidencia «{oRegistro.sReferencia}» porque tiene mantenimientos.')
        return super().unlink()
