# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CopiaLlave(models.Model):
    _name = 'upoferia.copia_llave'
    _description = 'Copia de llave'
    _rec_name = 'iNumeroCopia'

    iNumeroCopia = fields.Integer(string='Número de copia', required=True)
    dFechaBaja = fields.Date(string='Fecha de baja')
    sEstado = fields.Selection([
        ('activa', 'Activa'),
        ('devuelta', 'Devuelta'),
        ('perdida', 'Perdida'),
    ], string='Estado', required=True, default='activa')
    dFechaEntrega = fields.Date(string='Fecha de entrega')

    numero_y_fecha_inicio = fields.Many2one('upoferia.asignacion_taquilla', string='Asignación de taquilla', required=True)

    _sql_constraints = [
            ('asignacion_numero_copia_uniq', 'UNIQUE (asignacion_id, "iNumeroCopia")',
             'Esa asignación ya tiene una copia con ese número.'),
    ]

    @api.depends('iNumeroCopia')
    def _compute_display_name(self):
        oRegistro = None
        for oRegistro in self:
            oRegistro.display_name = f'Copia {oRegistro.iNumeroCopia}'

    @api.constrains('dFechaBaja', 'dFechaEntrega')
    def _check_fecha_baja(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.dFechaBaja and oRegistro.dFechaEntrega and oRegistro.dFechaBaja < oRegistro.dFechaEntrega:
                raise models.ValidationError('La «Fecha de baja» no puede ser anterior a la «Fecha de entrega».')
