from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TipoTransaccion(models.Model):
    _name = 'feria.tipo_transaccion'
    _description = 'Tipo de transacción'
    _rec_name = 'sCodigo'
    _sql_constraints = [
        ('codigo_uniq', 'UNIQUE ("sCodigo")',
         'Ya existe un tipo de transacción con ese código.'),
    ]

    sCodigo = fields.Char(string='Código', required=True)
    sDescripcion = fields.Char(string='Descripción')
    sNombre = fields.Char(string='Nombre')

    @api.constrains('sCodigo')
    def _check_codigo_valor(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.sCodigo not in ('PED', 'ALB', 'FAC', 'ABO', 'CON'):
                raise ValidationError('El código debe ser PED, ALB, FAC, ABO o CON.')
