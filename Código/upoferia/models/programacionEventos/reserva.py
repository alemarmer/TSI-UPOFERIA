from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Reserva(models.Model):
    _name = 'upoferia.reserva'
    _description = 'Upoferia.reserva'
    _rec_name = 'dHora_llegada'

    dHora_llegada = fields.Datetime(string='Hora de llegada', required=True)
    iNum_personas = fields.Integer(string='Número de personas')
    sEstado = fields.Selection([('pendiente', 'Pendiente'),
                               ('confirmada', 'Confirmada'),
                               ('cancelada', 'Cancelada'),
                               ('no_presentado', 'No presentado')],
                              string='Estado', default='pendiente')

    #MANY2ONE CON MESA (OJO ES TAMBIEN PK)
    #MANY2ONE CON SOCIO

    @api.constrains('iNum_personas')
    def _check_iNum_personas(self):
        for record in self:
            if record.iNum_personas <= 0:
                raise ValidationError('«Número de personas» debe ser mayor que 0.')




