from odoo import models,fields,api

class Caballo(models.Model):

    _name='upoferia.caballo' 
    _description='Upoferia.caballo'
    _sql_constraints = [
        ('microchip_uniq', 'UNIQUE (microchip)',
         'Ya existe un caballo con ese microchip.'),
    ]

    sMicrochip= fields.Char(string="Microchip del caballo", size=60, required=True) 
    sNombre = fields.Char(string="Nombre del caballo", size=100)
    sRaza = fields.Char(string="Raza del caballo", size=100)
    sSexo = fields.Char(string="Sexo del caballo", size=100)

    @api.constrains('microchip')
    def _check_microchip_formato(self):
        for record in self:
            if not re.fullmatch(r'[0-9]{15}', record.microchip or ''):
                raise ValidationError('El microchip debe tener 15 dígitos (norma ISO 11784/11785).')

    @api.constrains('nombre', 'raza', 'sexo')
    def _check_longitud(self):
        for record in self:
            for campo in ('nombre', 'raza', 'sexo'):
                if record[campo] and len(record[campo]) > 100:
                    raise ValidationError(
                        '«%s» no puede superar los 100 caracteres.' % record._fields[campo].string)

    @api.constrains('nombre', 'raza', 'sexo')
    def _check_textos_opcionales(self):
        for record in self:
            for campo in ('nombre', 'raza', 'sexo'):
                if record[campo] and not record[campo].strip():
                    raise ValidationError(
                        '«%s» no puede contener solo espacios.' % record._fields[campo].string)
