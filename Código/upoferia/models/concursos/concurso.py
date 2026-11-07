from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Concurso(models.Model):
    _name = 'upoferia.concurso'
    _description = 'Upoferia.Concurso'
    _inherits = {'upoferia.evento': 'evento_id'}
    _rec_name = 'sNombre_evento'
    _sql_constraints = [
        ('evento_uniq', 'UNIQUE ("evento_id")', 'Ese evento ya está registrado como concurso.'),
    ]

    sBases = fields.Text(string='Bases')
    dFecha_resultado = fields.Date(string='Fecha del resultado')
    # Lista cerrada según el E-R (Selection): valores por acordar en el grupo
    sEstado = fields.Selection([('abierto', 'Inscripción abierta'),
                               ('cerrado', 'Inscripción cerrada'),
                               ('resuelto', 'Resuelto')],
                              string='Estado', default='abierto')

    evento_id = fields.Many2one('upoferia.evento', string='Evento', required=True, ondelete='cascade')

    jurado_ids = fields.One2many('upoferia.jurado', 'concurso_id', string='Jurado')

    participacion_ids = fields.One2many('upoferia.participacion_concurso', 'concurso_id', string='Participantes')

    premio_ids = fields.One2many('upoferia.premio', 'concurso_id', string='Premios')

    @api.constrains('sBases')
    def _check_textos_opcionales(self):
        for record in self:
            for campo in ('sBases', 'sEstado'):
                if record[campo] and not record[campo].strip():
                    raise ValidationError(
                        '«%s» no puede contener solo espacios.' % record._fields[campo].string)
