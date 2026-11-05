from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Concurso(models.Model):
    _name = 'upoferia.concurso'
    _description = 'Upoferia.Concurso'
    _inherits = {'upoferia.evento': 'evento_id'}
    _rec_name = 'sNombre_evento'
    _sql_constraints = [
        ('evento_uniq', 'UNIQUE (evento_id)', 'Ese evento ya está registrado como concurso.'),
    ]

    sBases = fields.Text(string='Bases')
    dFecha_resultado = fields.Date(string='Fecha del resultado')
    # Lista cerrada según el E-R (Selection): valores por acordar en el grupo
    sEstado = fields.Char(string='Estado')

    evento_id = fields.Many2one('upoferia.evento', string='Evento', required=True, ondelete='cascade')

    jurado_ids = fields.One2many('upoferia.jurado', 'concurso_id', string='Jurado')

    @api.constrains('sEstado')
    def _check_longitud(self):
        for record in self:
            for campo in ('sEstado',):
                if record[campo] and len(record[campo]) > 100:
                    raise ValidationError(
                        '«%s» no puede superar los 100 caracteres.' % record._fields[campo].string)

    @api.constrains('sBases', 'sEstado')
    def _check_textos_opcionales(self):
        for record in self:
            for campo in ('sBases', 'sEstado'):
                if record[campo] and not record[campo].strip():
                    raise ValidationError(
                        '«%s» no puede contener solo espacios.' % record._fields[campo].string)
