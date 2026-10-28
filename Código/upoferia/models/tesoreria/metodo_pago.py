from odoo import models, fields


class MetodoPago(models.Model):

    _name = 'upoferia.metodo_pago'
    _description = 'Método de pago'
    _rec_name = 'nombre'

    nombre = fields.Char(string="Nombre", required=True, help="Identificador único del método de pago")
    comision_porcentaje = fields.Float(string="Comisión (%)", digits=(5, 2), default=0.0)
    activo = fields.Boolean(string="Activo", default=True)
    
    _sql_constraints = [
        ('nombre_unique', 'UNIQUE(nombre)', 'Ya existe un método de pago con ese nombre.'),
        ('comision_rango', 'CHECK(comision_porcentaje >= 0 AND comision_porcentaje <= 100)',
         'La comisión debe estar entre 0 y 100 %.'),
    ]

    @api.constrains('nombre')
    def _check_nombre(self):
        for record in self:
            if not record.nombre.strip():
                raise ValidationError('El nombre del método de pago no puede estar vacío.')

    @api.onchange('comision_porcentaje')
    def onchange_comision_porcentaje(self):
        if self.comision_porcentaje > 10:
            return {
                'warning': {
                    'title': 'Comisión elevada',
                    'message': 'Una comisión del %s %% es muy alta para un método de pago. Comprueba que es correcta.'
                               % self.comision_porcentaje
                }
            }

    @api.onchange('activo')
    def onchange_activo(self):
        if not self.activo:
            return {
                'warning': {
                    'title': 'Método de pago desactivado',
                    'message': 'No podrá usarse en nuevos movimientos, pero se conservan los que ya lo usan.'
                }
            }