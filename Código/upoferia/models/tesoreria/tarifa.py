from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class Tarifa(models.Model):

    _name = 'upoferia.tarifa'
    _description = 'Tarifa de precios'
    _rec_name = 'sNombre'

    sNombre = fields.Char(string="Nombre", required=True, help="Identificador único de la tarifa")
    sMoneda = fields.Char(string="Moneda", size=3, default='EUR', help="Código ISO de la moneda (EUR, USD…)")
    
    # Relaciones
    ticket_ids = fields.One2many('upoferia.ticket', 'tarifa_id', string="Tickets")

    _sql_constraints = [
        ('nombre_unique', 'UNIQUE("sNombre")', 'Ya existe una tarifa con ese nombre.'),
    ]

    @api.constrains('sNombre')
    def _check_nombre(self):
        for record in self:
            if not record.sNombre.strip():
                raise ValidationError('El nombre de la tarifa no puede estar vacío.')

    @api.constrains('sMoneda')
    def _check_moneda(self):
        for record in self:
            if record.sMoneda and not re.fullmatch(r'[A-Z]{3}', record.sMoneda):
                raise ValidationError('La moneda «%s» no es un código ISO válido: deben ser 3 letras, por ejemplo EUR.'
                                      % record.sMoneda)

    @api.onchange('sMoneda')
    def onchange_moneda(self):
        if self.sMoneda:
            self.sMoneda = self.sMoneda.strip().upper()
            if self.sMoneda != 'EUR':
                return {
                    'warning': {
                        'title': 'Moneda distinta del euro',
                        'message': 'La tarifa usará %s en lugar de EUR. Comprueba que es correcto.' % self.sMoneda
                    }
                }