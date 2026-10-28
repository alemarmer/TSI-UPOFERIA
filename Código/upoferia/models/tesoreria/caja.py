from odoo import models, fields


class Caja(models.Model):

    _name = 'upoferia.caja'
    _description = 'Caja o punto de cobro'
    _rec_name = 'nombre'

    nombre = fields.Char(string="Nombre", required=True, help="Identificador único de la caja")
    ubicacion = fields.Char(string="Ubicación")
    activa = fields.Boolean(string="Activa", default=True)
        
    _sql_constraints = [
        ('nombre_unique', 'UNIQUE(nombre)', 'Ya existe una caja con ese nombre.'),
    ]

    @api.constrains('nombre')
    def _check_nombre(self):
        for record in self:
            if not record.nombre.strip():
                raise ValidationError('El nombre de la caja no puede estar vacío.')

    @api.onchange('activa')
    def onchange_activa(self):
        if not self.activa:
            return {
                'warning': {
                    'title': 'Caja desactivada',
                    'message': 'La caja no podrá usarse en nuevos movimientos, pero se conservan los que ya tiene.'
                }
            }