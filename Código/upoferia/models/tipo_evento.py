from odoo import models,fields,api
from odoo.exceptions import ValidationError

class Tipo_evento(models.Model):

    _name='upoferia.tipo_evento' 
    _description='Upoferia.tipo_evento'

    sNombre_tipo_evento_tipo_evento= fields.Char(string="Nombre del tipo de evento", size=60, required=True) 
    sDescripcion = fields.Text(string="Descripción del tipo de evento", size=100)

    evento_ids = fields.One2many('upoferia.evento', 'tipo_evento_id', string='Eventos')

    @api.constrains('sNombre_tipo_evento')
    def _check_sNombre_tipo_evento_obligatorio(self):
        for record in self:
            if not (record.sNombre_tipo_evento or '').strip():
                raise ValidationError('El campo «sNombre_tipo_evento» es obligatorio.')

    @api.constrains('sNombre_tipo_evento', 'sDescripcion')
    def _check_longitud(self):
        for record in self:
            for campo in ('sNombre_tipo_evento', 'sDescripcion'):
                if record[campo] and len(record[campo]) > 100:
                    raise ValidationError(
                        '«%s» no puede superar los 100 caracteres.' % record._fields[campo].string)

    @api.constrains('sDescripcion')
    def _check_textos_opcionales(self):
        for record in self:
            for campo in ('sDescripcion',):
                if record[campo] and not record[campo].strip():
                    raise ValidationError(
                        '«%s» no puede contener solo espacios.' % record._fields[campo].string)

