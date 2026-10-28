from odoo import models, fields


class Presupuesto(models.Model):

    _name = 'upoferia.presupuesto'
    _description = 'Presupuesto anual'
    _rec_name = 'nombre'

    ejercicio = fields.Integer(string="Ejercicio", required=True, help="Identificador único del presupuesto (un presupuesto por año)")
    nombre = fields.Char(string="Nombre", required=True)
    fecha_inicio = fields.Date(string="Fecha de inicio", required=True)
    fecha_fin = fields.Date(string="Fecha de fin", required=True)
    estado = fields.Selection([('borrador', 'Borrador'),
                               ('aprobado', 'Aprobado'),
                               ('cerrado', 'Cerrado'),],
                              'Estado', default='borrador')