from odoo import models, fields, api
from datetime import date


class Presupuesto(models.Model):

    _name = 'upoferia.presupuesto'
    _description = 'Presupuesto anual'
    _rec_name = 'sNombre'

    iEjercicio = fields.Integer(string="Ejercicio", required=True, help="Identificador único del presupuesto (un presupuesto por año)")
    sNombre = fields.Char(string="Nombre", required=True)
    dFechaInicio = fields.Date(string="Fecha de inicio", required=True)
    dFechaFin = fields.Date(string="Fecha de fin", required=True)
    selEstado = fields.Selection([('borrador', 'Borrador'),
                               ('aprobado', 'Aprobado'),
                               ('cerrado', 'Cerrado'),],
                              'Estado', default='borrador')
    
    # Relaciones
    linea_ids = fields.One2many('upoferia.linea_presupuesto', 'presupuesto_id', string="Líneas de presupuesto")

    _sql_constraints = [
        ('ejercicio_unique', 'UNIQUE("iEjercicio")', 'Ya existe un presupuesto para ese ejercicio.'),
    ]

    @api.constrains('sNombre')
    def _check_nombre(self):
        for record in self:
            if not record.sNombre.strip():
                raise models.ValidationError('El nombre del presupuesto no puede estar vacío.')

    @api.constrains('iEjercicio', 'dFechaInicio', 'dFechaFin')
    def _check_ejercicio(self):
        for record in self:
            if not (2000 <= record.iEjercicio <= 2100):
                raise models.ValidationError('El ejercicio debe ser un año válido (2000-2100).')
            if record.dFechaFin < record.dFechaInicio:
                raise models.ValidationError('La fecha de fin no puede ser anterior a la de inicio.')
            if not (record.dFechaInicio.year <= record.iEjercicio <= record.dFechaFin.year):
                raise models.ValidationError('El periodo del presupuesto (%s – %s) no incluye el ejercicio %s.'
                                      % (record.dFechaInicio, record.dFechaFin, record.iEjercicio))

    @api.onchange('iEjercicio')
    def onchange_ejercicio(self):
        if self.iEjercicio and 2000 <= self.iEjercicio <= 2100:
            if not self.dFechaInicio:
                self.dFechaInicio = date(self.iEjercicio, 1, 1)
            if not self.dFechaFin:
                self.dFechaFin = date(self.iEjercicio, 12, 31)
            if not self.sNombre:
                self.sNombre = 'Presupuesto %s' % self.iEjercicio

    @api.onchange('dFechaInicio', 'dFechaFin')
    def onchange_fechas(self):
        if self.dFechaInicio and self.dFechaFin and self.dFechaFin < self.dFechaInicio:
            return {
                'value': {'dFechaFin': date(self.dFechaInicio.year, 12, 31)},
                'warning': {
                    'title': 'Fechas incorrectas',
                    'message': 'La fecha de fin era anterior a la de inicio; se ha puesto a fin de año.'
                }
            }

    @api.onchange('selEstado')
    def onchange_estado(self):
        if self._origin.id and self._origin.selEstado == 'cerrado' and self.selEstado != 'cerrado':
            return {
                'value': {'selEstado': 'cerrado'},
                'warning': {
                    'title': 'Presupuesto cerrado',
                    'message': 'Un presupuesto cerrado no puede reabrirse.'
                }
            }
        if self.selEstado == 'aprobado' and self._origin.selEstado == 'borrador':
            return {
                'warning': {
                    'title': 'Aprobar presupuesto',
                    'message': 'Una vez aprobado, sus líneas ya no podrán modificarse.'
                }
            }