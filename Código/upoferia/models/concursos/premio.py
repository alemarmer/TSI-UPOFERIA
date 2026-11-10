# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Premio(models.Model):
    _name = 'upoferia.premio'
    _description = 'Upoferia.premio'
    _rec_name = 'iPuesto'


    iPuesto = fields.Integer(string='Puesto', required=True)
    sDescripcion = fields.Char(string='Descripción')
    fImporte = fields.Float(string='Importe')
    iXp_otorgada = fields.Integer(string='XP otorgada')

    concurso_id = fields.Many2one('upoferia.concurso', string='Concurso', required=True)
    registro_xp_ids = fields.One2many('upoferia.registro_xp', 'premio_id', string='Registros de XP')

    _sql_constraints = [('premio_concurso_puesto_unique', 'UNIQUE ("concurso_id", "iPuesto")', 'Ese concurso ya tiene un premio para ese puesto.')]


    @api.constrains('iPuesto')
    def _check_iPuesto(self):
        for record in self:
            if record.iPuesto <= 0:
                raise models.ValidationError('«iPuesto» debe ser mayor que 0.')

    @api.constrains('fImporte')
    def _check_fImporte(self):
        for record in self:
            if record.fImporte < 0:
                raise models.ValidationError('«fImporte» no puede ser menor que 0.')

    @api.constrains('iXp_otorgada')
    def _check_iXp_otorgada(self):
        for record in self:
            if record.iXp_otorgada < 0:
                raise models.ValidationError('«XP otorgada» no puede ser menor que 0.')

    @api.constrains('sDescripcion')
    def _check_sDescripcion_espacios(self):
        for record in self:
            if record.sDescripcion and not record.sDescripcion.strip():
                raise models.ValidationError('«Descripción» no puede contener solo espacios.')

    @api.constrains('sDescripcion')
    def _check_sDescripcion_longitud(self):
        for record in self:
            if record.sDescripcion and len(record.sDescripcion) > 100:
                raise models.ValidationError('«Descripción» no puede superar los 100 caracteres.')