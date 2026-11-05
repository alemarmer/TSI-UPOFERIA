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
    sNombre = fields.Char(string='Nombre', required=True)

    transaccion_ids = fields.One2many('feria.transaccion', 'tipo_transaccion_id', string='Transacciones')

    @api.constrains('sCodigo')
    def _check_codigo_valor(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.sCodigo not in ('PED', 'ALB', 'FAC', 'ABO', 'CON'):
                raise ValidationError('El código debe ser PED, ALB, FAC, ABO o CON.')

    @api.constrains('sNombre')
    def _check_nombre(self):
        oRegistro = None
        sNombre = ''
        for oRegistro in self:
            sNombre = oRegistro.sNombre or ''
            if not sNombre.strip():
                raise ValidationError('El campo «Nombre» del tipo de transacción es obligatorio.')
            if sNombre != sNombre.strip():
                raise ValidationError('El nombre del tipo de transacción no puede empezar ni terminar con espacios.')
            if not 2 <= len(sNombre) <= 50:
                raise ValidationError('El nombre del tipo de transacción debe tener entre 2 y 50 caracteres.')

    @api.constrains('sDescripcion')
    def _check_descripcion(self):
        oRegistro = None
        sDescripcion = ''
        for oRegistro in self:
            sDescripcion = oRegistro.sDescripcion or ''
            if not sDescripcion:
                continue
            if sDescripcion != sDescripcion.strip():
                raise ValidationError('La descripción del tipo de transacción no puede empezar ni terminar con espacios.')
            if len(sDescripcion) > 255:
                raise ValidationError('La descripción del tipo de transacción no puede tener más de 255 caracteres.')
