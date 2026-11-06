from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TipoProducto(models.Model):

    _name = 'upoferia.tipo_producto'
    _description = 'Tipo de producto'
    _rec_name = 'nombre'

    nombre = fields.Char(string="Nombre", required=True, help="Identificador único del tipo de producto")
    
    # Relaciones
    padre_id = fields.Many2one('upoferia.tipo_producto', string="Tipo padre", ondelete='restrict')
    hijo_ids = fields.One2many('upoferia.tipo_producto', 'padre_id', string="Subtipos")
    producto_ids = fields.One2many('upoferia.producto', 'tipo_producto_id', string="Productos")

    _sql_constraints = [
        ('nombre_unique', 'UNIQUE(nombre)', 'Ya existe un tipo de producto con ese nombre.'),
    ]

    @api.constrains('nombre')
    def _check_nombre(self):
        for record in self:
            if not record.nombre.strip():
                raise ValidationError('El nombre del tipo de producto no puede estar vacío.')

    @api.onchange('nombre')
    def onchange_nombre(self):
        if self.nombre:
            self.nombre = ' '.join(self.nombre.split()).capitalize()