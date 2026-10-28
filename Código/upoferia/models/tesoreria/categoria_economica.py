from odoo import models, fields


class CategoriaEconomica(models.Model):

    _name = 'upoferia.categoria_economica'
    _description = 'Categoría económica'
    _rec_name = 'nombre'

    nombre = fields.Char(string="Nombre", required=True, help="Identificador único de la categoría económica")
    tipo = fields.Selection([('ingreso', 'Ingreso'),
                             ('gasto', 'Gasto'),],
                            'Tipo', required=True)