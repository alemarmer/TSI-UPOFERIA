from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Premio(models.Model):
    _name = 'upoferia.premio'
    _description = 'Upoferia.premio'
    _rec_name = 'iPuesto'
    _sql_constraints = [
        # PK compuesta (nombre_concurso, iPuesto)
        ('concurso_iPuesto_uniq', 'UNIQUE (concurso_id, iPuesto)',
         'Ese concurso ya tiene un premio para ese Puesto.'),
    ]

    iPuesto = fields.Integer(string='Puesto', required=True)
    sDescripcion = fields.Char(string='Descripción')
    fImporte = fields.Float(string='Importe')
    iXp_otorgada = fields.Integer(string='XP otorgada')

    concurso_id = fields.Many2one('upoferia.concurso', string='Concurso',
                                  required=True, ondelete='cascade')

    #ojo relacion con REGISTRO_XP

    @api.constrains('iPuesto')
    def _check_iPuesto(self):
        for record in self:
            if record.iPuesto <= 0:
                raise ValidationError('«iPuesto» debe ser mayor que 0.')

    @api.constrains('fImporte')
    def _check_fImporte(self):
        for record in self:
            if record.fImporte < 0:
                raise ValidationError('«fImporte» no puede ser menor que 0.')

    @api.constrains('iXp_otorgada')
    def _check_iXp_otorgada(self):
        for record in self:
            if record.iXp_otorgada < 0:
                raise ValidationError('«XP otorgada» no puede ser menor que 0.')

    @api.constrains('sDescripcion')
    def _check_sDescripcion_espacios(self):
        for record in self:
            if record.sDescripcion and not record.sDescripcion.strip():
                raise ValidationError('«Descripción» no puede contener solo espacios.')

    @api.constrains('sDescripcion')
    def _check_sDescripcion_longitud(self):
        for record in self:
            if record.sDescripcion and len(record.sDescripcion) > 100:
                raise ValidationError('«Descripción» no puede superar los 100 caracteres.')