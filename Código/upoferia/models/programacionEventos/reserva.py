# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Reserva(models.Model):
    _name = 'upoferia.reserva'
    _description = 'Reserva'
    _rec_name = 'dHora_llegada'

    dHora_llegada = fields.Datetime(string='Hora de llegada', required=True)
    iNum_personas = fields.Integer(string='Número de personas')
    sEstado = fields.Selection([('pendiente', 'Pendiente'),
                                ('confirmada', 'Confirmada'),
                                ('cancelada', 'Cancelada'),
                                ('no_presentado', 'No presentado')],
                               'Estado', default='pendiente')

    #MANY2ONE CON MESA (OJO ES TAMBIEN PK)
    #MANY2ONE CON SOCIO

    def btn_submit_to_pendiente(self):
        self.write({'sEstado': 'pendiente'})

    def btn_submit_to_confirmada(self):
        self.write({'sEstado': 'confirmada'})

    def btn_submit_to_cancelada(self):
        self.write({'sEstado': 'cancelada'})

    def btn_submit_to_no_presentado(self):
        self.write({'sEstado': 'no_presentado'})

    @api.constrains('iNum_personas')
    def _check_iNum_personas(self):
        for record in self:
            if record.iNum_personas <= 0:
                raise models.ValidationError('El número de personas debe ser mayor que 0.')
