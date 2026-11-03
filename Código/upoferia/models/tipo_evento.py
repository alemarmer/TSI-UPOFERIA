from odoo import models,fields,api

class Tipo_evento(models.Model):

    _name='upoferia.tipo_evento' 
    _description='Upoferia.tipo_evento'

    sNombre= fields.Char(string="Nombre del tipo de evento", size=60, required=True) 
    sDescripcion = fields.Text(string="Nombre del tipo de evento", size=100)

    @api.constrains('nombre')
    def _check_nombre_obligatorio(self):
        for record in self:
            if not (record.nombre or '').strip():
                raise ValidationError('El campo «Nombre» es obligatorio.')

    @api.constrains('nombre', 'descripcion')
    def _check_longitud(self):
        for record in self:
            for campo in ('nombre', 'descripcion'):
                if record[campo] and len(record[campo]) > 100:
                    raise ValidationError(
                        '«%s» no puede superar los 100 caracteres.' % record._fields[campo].string)

    @api.constrains('descripcion')
    def _check_textos_opcionales(self):
        for record in self:
            for campo in ('descripcion',):
                if record[campo] and not record[campo].strip():
                    raise ValidationError(
                        '«%s» no puede contener solo espacios.' % record._fields[campo].string)

