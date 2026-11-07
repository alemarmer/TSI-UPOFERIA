from odoo import models,fields,api
from odoo.exceptions import ValidationError

class Evento(models.Model):

    _name='upoferia.evento' 
    _description='Upoferia.evento'

    sNombre_evento= fields.Char(string="Nombre del evento", size=60, required=True) #obligatorio para todas las clases de python, y simula la pk. odoo por dentro lo hace pk. Si la pk es dni, se cambia en string no en el sNombre_evento
    dFecha_hora_inicio = fields.Datetime(string='Fecha y hora de inicio')
    dFecha_hora_fin = fields.Datetime(string='Fecha y hora de finalizacion')
    iAforo_reservado = fields.Integer(string='Aforo reservado')
    sEstado = fields.Selection([('programado', 'Programado'),
                               ('en_curso', 'En curso'),
                               ('finalizado', 'Finalizado'),
                               ('cancelado', 'Cancelado')],
                              string='Estado', default='programado')

    #FK CON CASETA

    tipo_evento_id = fields.Many2one('upoferia.tipo_evento', string='Tipo de evento',
                                     required=True, ondelete='restrict')

    concurso_ids = fields.One2many('upoferia.concurso', 'evento_id', string='Concurso')

    #OJO CONEXION CON ACTUACION 
    #patrocinio_ids = fields.One2many('upoferia.patrocinio', 'evento_id', string='Patrocinios')

    @api.constrains('sNombre_evento')
    def _check_sNombre_evento_obligatorio(self):
        for record in self:
            if not (record.sNombre_evento or '').strip():
                raise ValidationError('El campo «sNombre_evento» es obligatorio.')

    @api.constrains('dFecha_hora_inicio', 'dFecha_hora_fin')
    def _check_dFecha_hora_fin(self):
        for record in self:
            if record.dFecha_hora_inicio and record.dFecha_hora_fin and record.dFecha_hora_fin <= record.dFecha_hora_inicio:
                raise ValidationError('«dFecha_hora_fin» debe ser posterior a «Hora de inicio».')


    @api.constrains('iAforo_reservado')
    def _check_iAforo_reservado(self):
        for record in self:
            if record.iAforo_reservado < 0:
                raise ValidationError('«Aforo reservado» no puede ser menor que 0.')

    @api.constrains('dFecha_hora_fin', 'dFecha_hora_inicio')
    def _check_dFecha_hora_inicio_si_dFecha_hora_fin(self):
        for record in self:
            if record.dFecha_hora_fin and not record.dFecha_hora_inicio:
                raise ValidationError('Si se indica «dFecha_hora_fin», también hay que indicar «Hora de inicio».')

    @api.constrains('sNombre_evento')
    def _check_longitud(self):
        for record in self:
            for campo in ('sNombre_evento','sEstado'):
                if record[campo] and len(record[campo]) > 100:
                    raise ValidationError(
                        '«%s» no puede superar los 100 caracteres.' % record._fields[campo].string)



