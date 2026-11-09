from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MetodoPago(models.Model):

    _name = 'upoferia.metodo_pago'
    _description = 'Método de pago'
    _rec_name = 'sNombre'

    sNombre = fields.Char(string="Nombre", required=True, help="Identificador único del método de pago")
    fComisionPorcentaje = fields.Float(string="Comisión (%)", digits=(5, 2), default=0.0)
    bActivo = fields.Boolean(string="Activo", default=True)
    
    # Relaciones
    movimiento_ids = fields.One2many('upoferia.movimiento', 'metodo_pago_id', string="Movimientos")

    _sql_constraints = [
        ('nombre_unique', 'UNIQUE("sNombre")', 'Ya existe un método de pago con ese nombre.'),
    ]

    @api.constrains('sNombre')
    def _check_nombre(self):
        for record in self:
            if not record.sNombre.strip():
                raise ValidationError('El nombre del método de pago no puede estar vacío.')

    @api.constrains('fComisionPorcentaje')
    def _check_comision_porcentaje(self):
        for record in self:
            if not (0 <= record.fComisionPorcentaje <= 100):
                raise ValidationError('La comisión debe estar entre 0 y 100 %.')

    @api.onchange('fComisionPorcentaje')
    def onchange_comision_porcentaje(self):
        if self.fComisionPorcentaje > 10:
            return {
                'warning': {
                    'title': 'Comisión elevada',
                    'message': 'Una comisión del %s %% es muy alta para un método de pago. Comprueba que es correcta.'
                               % self.fComisionPorcentaje
                }
            }

    @api.onchange('bActivo')
    def onchange_activo(self):
        if not self.bActivo:
            return {
                'warning': {
                    'title': 'Método de pago desactivado',
                    'message': 'No podrá usarse en nuevos movimientos, pero se conservan los que ya lo usan.'
                }
            }