from odoo import models, fields


class CategoriaEconomica(models.Model):

    _name = 'upoferia.categoria_economica'
    _description = 'Categoría económica'
    _rec_name = 'nombre'

    nombre = fields.Char(string="Nombre", required=True, help="Identificador único de la categoría económica")
    tipo = fields.Selection([('ingreso', 'Ingreso'),
                             ('gasto', 'Gasto'),],
                            'Tipo', required=True)
    
    _sql_constraints = [
        ('nombre_unique', 'UNIQUE(nombre)', 'Ya existe una categoría económica con ese nombre.'),
    ]

    @api.constrains('nombre')
    def _check_nombre(self):
        for record in self:
            if not record.nombre.strip():
                raise ValidationError('El nombre de la categoría económica no puede estar vacío.')

    @api.onchange('tipo')
    def onchange_tipo(self):
        if self._origin.id and self._origin.tipo and self.tipo != self._origin.tipo:
            return {
                'warning': {
                    'title': 'Cambio de tipo',
                    'message': 'Esta categoría ya existía como «%s». Cambiar su tipo afecta a las líneas de presupuesto '
                               'y movimientos que la usan.' % dict(self._fields['tipo'].selection).get(self._origin.tipo)
                }
            }