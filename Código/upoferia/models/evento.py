from odoo import models,fields,api
from odoo.exceptions import ValidationError

class Evento(models.Model):

    _name='upoferia.evento' 
    _description='Upoferia.evento'

    sNombre_evento= fields.Char(string="Nombre del evento", size=60, required=True) #obligatorio para todas las clases de python, y simula la pk. odoo por dentro lo hace pk. Si la pk es dni, se cambia en string no en el nombre
    dFecha_hora_inicio = fields.Datetime(string='Fecha y hora de inicio')
    dFecha_hora_fin = fields.Datetime(string='Fecha y hora de finalizacion')
    iAforo_reservado = fields.Integer(string='Aforo reservado')
    sEstado = fields.Char(string='Estado')

    @api.constrains('nombre')
    def _check_nombre_obligatorio(self):
        for record in self:
            if not (record.nombre or '').strip():
                raise ValidationError('El campo «Nombre» es obligatorio.')

    @api.constrains('hora_inicio', 'fin')
    def _check_fin(self):
        for record in self:
            if record.hora_inicio and record.fin and record.fin <= record.hora_inicio:
                raise ValidationError('«Fin» debe ser posterior a «Hora de inicio».')


    @api.constrains('aforo_reservado')
    def _check_aforo_reservado(self):
        for record in self:
            if record.aforo_reservado < 0:
                raise ValidationError('«Aforo reservado» no puede ser menor que 0.')

    @api.constrains('fin', 'hora_inicio')
    def _check_hora_inicio_si_fin(self):
        for record in self:
            if record.fin and not record.hora_inicio:
                raise ValidationError('Si se indica «Fin», también hay que indicar «Hora de inicio».')

    @api.constrains('nombre', 'tipo', 'estado')
    def _check_longitud(self):
        for record in self:
            for campo in ('nombre', 'tipo', 'estado'):
                if record[campo] and len(record[campo]) > 100:
                    raise ValidationError(
                        '«%s» no puede superar los 100 caracteres.' % record._fields[campo].string)

    @api.constrains('tipo', 'estado')
    def _check_textos_opcionales(self):
        for record in self:
            for campo in ('tipo', 'estado'):
                if record[campo] and not record[campo].strip():
                    raise ValidationError(
                        '«%s» no puede contener solo espacios.' % record._fields[campo].string)

