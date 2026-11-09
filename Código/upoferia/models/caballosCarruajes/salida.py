from odoo import models, fields, api


class Salida(models.Model):
    _name = 'upoferia.salida'
    _description = 'Salida de carruaje'
    _rec_name = 'dFecha_hora_salida'

    dFecha_hora_salida = fields.Datetime(string='Fecha y hora de salida', required=True)
    dFecha_hora_vuelta = fields.Datetime(string='Fecha y hora de vuelta')
    iNum_pasajeros = fields.Integer(string='Número de pasajeros')
    sEstado = fields.Selection([('programada', 'Programada'),
                                ('en_curso', 'En curso'),
                                ('finalizada', 'Finalizada'),
                                ('cancelada', 'Cancelada')],
                               'Estado', default='programada')

    carruaje_id = fields.Many2one('upoferia.carruaje', string='Carruaje', required=True)
    caballo_ids = fields.Many2many('upoferia.caballo', 'upoferia_salida_caballo',
                                   'salida_id', 'caballo_id', string='Caballos')

    iPlazas_libres = fields.Integer(compute='_plazasLibres', string='Plazas libres', store=True)

    transaccion_id = fields.Many2one('upoferia.transaccion', string='Transacción')

    _sql_constraints = [('salida_carruaje_fecha_unique', 'UNIQUE ("carruaje_id", "dFecha_hora_salida")', 'Ese carruaje ya tiene una salida a esa fecha y hora.')]

    def btn_submit_to_programada(self):
        self.write({'sEstado': 'programada'})

    def btn_submit_to_en_curso(self):
        self.write({'sEstado': 'en_curso'})

    def btn_submit_to_finalizada(self):
        self.write({'sEstado': 'finalizada'})

    def btn_submit_to_cancelada(self):
        self.write({'sEstado': 'cancelada'})
        for caballo in self.caballo_ids:
            self.write({'caballo_ids': [(3, caballo.id)]})

    def btn_quitarCaballos(self):
        for caballo in self.caballo_ids:
            self.write({'caballo_ids': [(3, caballo.id)]})

    @api.depends('carruaje_id.iPlazas', 'iNum_pasajeros')
    def _plazasLibres(self):
        for record in self:
            record.iPlazas_libres = record.carruaje_id.iPlazas - record.iNum_pasajeros

    @api.constrains('dFecha_hora_salida', 'dFecha_hora_vuelta')
    def _check_dFecha_hora_vuelta(self):
        for record in self:
            if record.dFecha_hora_vuelta and record.dFecha_hora_vuelta <= record.dFecha_hora_salida:
                raise models.ValidationError('La vuelta debe ser posterior a la salida.')

    @api.constrains('iNum_pasajeros', 'carruaje_id')
    def _check_iNum_pasajeros(self):
        for record in self:
            if record.iNum_pasajeros < 0:
                raise models.ValidationError('El número de pasajeros no puede ser negativo.')
            if record.iNum_pasajeros > record.carruaje_id.iPlazas:
                raise models.ValidationError('Hay más pasajeros que plazas tiene el carruaje.')

    @api.onchange('dFecha_hora_salida', 'dFecha_hora_vuelta')
    def onchange_fechas(self):
        resultado = {}
        if self.dFecha_hora_salida and self.dFecha_hora_vuelta and self.dFecha_hora_vuelta <= self.dFecha_hora_salida:
            resultado = {
                'warning': {
                    'title': 'Valores incorrectos',
                    'message': 'La vuelta debe ser posterior a la salida.'
                }
            }
        return resultado

    @api.onchange('carruaje_id', 'iNum_pasajeros')
    def onchange_pasajeros(self):
        resultado = {}
        if self.carruaje_id and self.iNum_pasajeros > self.carruaje_id.iPlazas:
            resultado = {
                'value': {'iNum_pasajeros': self.carruaje_id.iPlazas},
                'warning': {
                    'title': 'Valores incorrectos',
                    'message': 'El carruaje solo tiene %s plazas.' % self.carruaje_id.iPlazas
                }
            }
        return resultado
