from odoo import models, fields


class Cuota(models.Model):

    _name = 'upoferia.cuota'
    _description = 'Cuota de socio'
    _rec_name = 'referencia'

    referencia = fields.Char(string="Referencia", required=True, help="Identificador único de la cuota")
    ejercicio = fields.Integer(string="Ejercicio", required=True)
    fecha_emision = fields.Date(string="Fecha de emisión", required=True)
    fecha_vencimiento = fields.Date(string="Fecha de vencimiento", required=True)
    periodicidad = fields.Selection([('anual', 'Anual'),
                                     ('mensual', 'Mensual'),
                                     ('unica', 'Única'),],
                                    'Periodicidad', default='anual')