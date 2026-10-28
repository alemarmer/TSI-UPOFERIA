from odoo import models, fields


class Presupuesto(models.Model):

    _name = 'upoferia.presupuesto'
    _description = 'Presupuesto anual'
    _rec_name = 'nombre'

    ejercicio = fields.Integer(string="Ejercicio", required=True, help="Identificador único del presupuesto (un presupuesto por año)")
    nombre = fields.Char(string="Nombre", required=True)
    fecha_inicio = fields.Date(string="Fecha de inicio", required=True)
    fecha_fin = fields.Date(string="Fecha de fin", required=True)
    estado = fields.Selection([('borrador', 'Borrador'),
                               ('aprobado', 'Aprobado'),
                               ('cerrado', 'Cerrado'),],
                              'Estado', default='borrador')
    
    _sql_constraints = [
        ('ejercicio_unique', 'UNIQUE(ejercicio)', 'Ya existe un presupuesto para ese ejercicio.'),
        ('ejercicio_rango', 'CHECK(ejercicio BETWEEN 2000 AND 2100)', 'El ejercicio debe ser un año válido (2000-2100).'),
        ('fechas_orden', 'CHECK(fecha_fin >= fecha_inicio)', 'La fecha de fin no puede ser anterior a la de inicio.'),
    ]

    @api.constrains('nombre')
    def _check_nombre(self):
        for record in self:
            if not record.nombre.strip():
                raise ValidationError('El nombre del presupuesto no puede estar vacío.')

    @api.constrains('ejercicio', 'fecha_inicio', 'fecha_fin')
    def _check_ejercicio(self):
        for record in self:
            if not (record.fecha_inicio.year <= record.ejercicio <= record.fecha_fin.year):
                raise ValidationError('El periodo del presupuesto (%s – %s) no incluye el ejercicio %s.'
                                      % (record.fecha_inicio, record.fecha_fin, record.ejercicio))

    @api.onchange('ejercicio')
    def onchange_ejercicio(self):
        if self.ejercicio and 2000 <= self.ejercicio <= 2100:
            if not self.fecha_inicio:
                self.fecha_inicio = date(self.ejercicio, 1, 1)
            if not self.fecha_fin:
                self.fecha_fin = date(self.ejercicio, 12, 31)
            if not self.nombre:
                self.nombre = 'Presupuesto %s' % self.ejercicio

    @api.onchange('fecha_inicio', 'fecha_fin')
    def onchange_fechas(self):
        if self.fecha_inicio and self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            return {
                'value': {'fecha_fin': date(self.fecha_inicio.year, 12, 31)},
                'warning': {
                    'title': 'Fechas incorrectas',
                    'message': 'La fecha de fin era anterior a la de inicio; se ha puesto a fin de año.'
                }
            }

    @api.onchange('estado')
    def onchange_estado(self):
        if self._origin.id and self._origin.estado == 'cerrado' and self.estado != 'cerrado':
            return {
                'value': {'estado': 'cerrado'},
                'warning': {
                    'title': 'Presupuesto cerrado',
                    'message': 'Un presupuesto cerrado no puede reabrirse.'
                }
            }
        if self.estado == 'aprobado' and self._origin.estado == 'borrador':
            return {
                'warning': {
                    'title': 'Aprobar presupuesto',
                    'message': 'Una vez aprobado, sus líneas ya no podrán modificarse.'
                }
            }