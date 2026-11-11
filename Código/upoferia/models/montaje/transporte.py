# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Transporte(models.Model):

    _name = 'upoferia.transporte'
    _description = 'Transporte'
    _rec_name = 'sNumero'

    sNumero = fields.Char(string='Número', required=True, help='Identificador único del transporte')
    dtFechaPrevista = fields.Datetime(string='Fecha prevista')
    dtFechaRealizada = fields.Datetime(string='Fecha realizada')
    selEstado = fields.Selection([('pendiente', 'Pendiente'),
                                  ('en_ruta', 'En ruta'),
                                  ('entregado', 'Entregado'),],
                                 'Estado', default='pendiente')
    sTipoOperacion = fields.Char(string='Tipo de operación', default='Transferencia interna')
    sUbicacionOrigen = fields.Char(string='Ubicación de origen')
    sUbicacionDestino = fields.Char(string='Ubicación de destino')

    # Relaciones
    tarea_montaje_id = fields.Many2one('upoferia.tarea_montaje', string='Tarea de montaje')

    _sql_constraints = [
        ('numero_unique', 'UNIQUE("sNumero")', 'Ya existe un transporte con ese número.'),
    ]

    @api.constrains('sNumero')
    def _check_numero(self):
        for record in self:
            if not record.sNumero.strip():
                raise models.ValidationError('El número del transporte no puede estar vacío.')

    @api.onchange('selEstado')
    def onchange_estado(self):
        if self.selEstado == 'entregado' and not self.dtFechaRealizada:
            self.dtFechaRealizada = fields.Datetime.now()
