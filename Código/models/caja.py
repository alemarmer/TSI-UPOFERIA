from odoo import models, fields, api


class Caja(models.Model):

    _name = 'upoferia.caja'
    _description = 'Caja o punto de cobro'
    _rec_name = 'sNombre'

    sNombre = fields.Char(string="Nombre", required=True, help="Identificador único de la caja")
    sUbicacion = fields.Char(string="Ubicación")
    bActiva = fields.Boolean(string="Activa", default=True)
        
    # Relaciones
    movimiento_ids = fields.One2many('upoferia.movimiento', 'caja_id', string="Movimientos")

    _sql_constraints = [
        ('nombre_unique', 'UNIQUE("sNombre")', 'Ya existe una caja con ese nombre.'),
    ]

    @api.constrains('sNombre')
    def _check_nombre(self):
        for record in self:
            if not record.sNombre.strip():
                raise models.ValidationError('El nombre de la caja no puede estar vacío.')

    @api.onchange('bActiva')
    def onchange_activa(self):
        if not self.bActiva:
            return {
                'warning': {
                    'title': 'Caja desactivada',
                    'message': 'La caja no podrá usarse en nuevos movimientos, pero se conservan los que ya tiene.'
                }
            }