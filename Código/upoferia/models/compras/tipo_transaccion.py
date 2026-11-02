# -*- coding: utf-8 -*-
# Tabla TIPO_TRANSACCION del modelo relacional · bloque COMPRAS A PROVEEDORES
# Validaciones de atributo: implementadas al final de la clase.

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TipoTransaccion(models.Model):
    _name = 'feria.tipo_transaccion'
    _description = 'Tipo de transacción'
    _rec_name = 'codigo'
    _sql_constraints = [
        ('codigo_uniq', 'UNIQUE (codigo)',
         'Ya existe un tipo de transacción con ese código.'),
    ]

    # Según el E-R: PED, ALB, FAC, ABO, CON (son datos de la tabla)
    codigo = fields.Char(string='Código', required=True)
    descripcion = fields.Char(string='Descripción')
    nombre = fields.Char(string='Nombre')

    # Valores permitidos de «Código» (E-R)
    @api.constrains('codigo')
    def _check_codigo_valor(self):
        for record in self:
            if record.codigo not in ('PED', 'ALB', 'FAC', 'ABO', 'CON'):
                raise ValidationError('El código debe ser PED, ALB, FAC, ABO o CON.')
