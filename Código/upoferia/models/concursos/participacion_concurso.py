
from odoo import models, fields


class ParticipacionConcurso(models.Model):
    _name = 'upoferia.participacion_concurso'
    _description = 'Upoferia.participación_concurso'
    _sql_constraints = [
        ('socio_concurso_uniq', 'UNIQUE ("concurso_id")',
         'Ese socio ya está inscrito en ese concurso.'),
    ]
    """
        _sql_constraints = [
        ('socio_concurso_uniq', 'UNIQUE ("socio_id", "concurso_id")',
         'Ese socio ya está inscrito en ese concurso.'),
    ]
    """

    fecha = fields.Date(string='Fecha de inscripción')

    #socio_id = fields.Many2one('upoferia.socio', string='Socio', required=True, ondelete='cascade')
    concurso_id = fields.Many2one('upoferia.concurso', string='Concurso', required=True, ondelete='cascade')
