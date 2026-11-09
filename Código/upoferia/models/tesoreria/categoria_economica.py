from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CategoriaEconomica(models.Model):

    _name = 'upoferia.categoria_economica'
    _description = 'Categoría económica'
    _rec_name = 'sNombre'

    sNombre = fields.Char(string="Nombre", required=True, help="Identificador único de la categoría económica")
    selTipo = fields.Selection([('ingreso', 'Ingreso'),
                             ('gasto', 'Gasto'),],
                            'Tipo', required=True)
    
    # Relaciones
    linea_presupuesto_ids = fields.One2many('upoferia.linea_presupuesto', 'categoria_economica_id', string="Líneas de presupuesto")
    movimiento_ids = fields.One2many('upoferia.movimiento', 'categoria_economica_id', string="Movimientos")

    _sql_constraints = [
        ('nombre_unique', 'UNIQUE("sNombre")', 'Ya existe una categoría económica con ese nombre.'),
    ]

    @api.constrains('sNombre')
    def _check_nombre(self):
        for record in self:
            if not record.sNombre.strip():
                raise ValidationError('El nombre de la categoría económica no puede estar vacío.')

    @api.onchange('selTipo')
    def onchange_tipo(self):
        if self._origin.id and self._origin.selTipo and self.selTipo != self._origin.selTipo:
            return {
                'warning': {
                    'title': 'Cambio de tipo',
                    'message': 'Esta categoría ya existía como «%s». Cambiar su tipo afecta a las líneas de presupuesto '
                               'y movimientos que la usan.' % dict(self._fields['selTipo'].selection).get(self._origin.selTipo)
                }
            }