from odoo import models, fields


class Tarifa(models.Model):

    _name = 'upoferia.tarifa'
    _description = 'Tarifa de precios'
    _rec_name = 'nombre'

    nombre = fields.Char(string="Nombre", required=True, help="Identificador único de la tarifa")
    moneda = fields.Char(string="Moneda", size=3, default='EUR', help="Código ISO de la moneda (EUR, USD…)")
    
    _sql_constraints = [
        ('nombre_unique', 'UNIQUE(nombre)', 'Ya existe una tarifa con ese nombre.'),
    ]

    @api.constrains('nombre')
    def _check_nombre(self):
        for record in self:
            if not record.nombre.strip():
                raise ValidationError('El nombre de la tarifa no puede estar vacío.')

    @api.constrains('moneda')
    def _check_moneda(self):
        for record in self:
            if record.moneda and not re.fullmatch(r'[A-Z]{3}', record.moneda):
                raise ValidationError('La moneda «%s» no es un código ISO válido: deben ser 3 letras, por ejemplo EUR.'
                                      % record.moneda)

    @api.onchange('moneda')
    def onchange_moneda(self):
        if self.moneda:
            self.moneda = self.moneda.strip().upper()
            if self.moneda != 'EUR':
                return {
                    'warning': {
                        'title': 'Moneda distinta del euro',
                        'message': 'La tarifa usará %s en lugar de EUR. Comprueba que es correcto.' % self.moneda
                    }
                }