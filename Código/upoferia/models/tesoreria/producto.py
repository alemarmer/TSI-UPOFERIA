from odoo import models, fields


class Producto(models.Model):

    _name = 'upoferia.producto'
    _description = 'Producto de barra'
    _rec_name = 'nombre'

    codigo_interno = fields.Char(string="Código interno", required=True, help="Identificador único del producto")
    nombre = fields.Char(string="Nombre", required=True)
    alergenos = fields.Char(string="Alérgenos")
    precio_socio = fields.Float(string="Precio socio", digits=(10, 2))
    xp_otorgada = fields.Integer(string="XP otorgada", default=0)
    
    _sql_constraints = [
        ('codigo_interno_unique', 'UNIQUE(codigo_interno)', 'Ya existe un producto con ese código interno.'),
        ('precio_socio_no_negativo', 'CHECK(precio_socio >= 0)', 'El precio de socio no puede ser negativo.'),
        ('xp_no_negativa', 'CHECK(xp_otorgada >= 0)', 'La experiencia otorgada no puede ser negativa.'),
    ]

    @api.constrains('codigo_interno')
    def _check_codigo_interno(self):
        for record in self:
            if not re.fullmatch(r'[A-Z0-9_-]+', record.codigo_interno or ''):
                raise ValidationError('El código interno «%s» solo puede contener letras mayúsculas, números, '
                                      'guiones y guiones bajos, sin espacios.' % record.codigo_interno)

    @api.constrains('nombre')
    def _check_nombre(self):
        for record in self:
            if not record.nombre.strip():
                raise ValidationError('El nombre del producto no puede estar vacío.')

    @api.onchange('codigo_interno')
    def onchange_codigo_interno(self):
        if self.codigo_interno:
            self.codigo_interno = self.codigo_interno.strip().upper().replace(' ', '_')

    @api.onchange('precio_socio')
    def onchange_precio_socio(self):
        if self.precio_socio < 0:
            return {
                'value': {'precio_socio': 0.0},
                'warning': {
                    'title': 'Precio incorrecto',
                    'message': 'El precio de socio no puede ser negativo.'
                }
            }

    @api.onchange('xp_otorgada')
    def onchange_xp_otorgada(self):
        if self.xp_otorgada < 0:
            return {
                'value': {'xp_otorgada': 0},
                'warning': {
                    'title': 'Experiencia incorrecta',
                    'message': 'La experiencia otorgada no puede ser negativa.'
                }
            }
        if self.xp_otorgada > 500:
            return {
                'warning': {
                    'title': 'Experiencia elevada',
                    'message': 'Este producto da %s puntos de experiencia por unidad. Comprueba que no es una errata.'
                               % self.xp_otorgada
                }
            }