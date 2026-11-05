from odoo import models,fields,api
from odoo.exceptions import ValidationError

class Artista(models.Model):
    _name = 'upoferia.artista'
    _description = 'Upoferia.artista'

    #poner dni como FK

    sDni= fields.Char(string="DNI del artista", size=60, required=True)
    fCache_base = fields.Float(string='Caché base')
    sMontaje = fields.Char(string='Montaje')
    sIluminacion = fields.Char(string='Iluminación')
    fPotencia_kw = fields.Float(string='Potencia (kW)')
    sSonido = fields.Char(string='Sonido')
    sEspacio = fields.Char(string='Espacio')

    disciplina_nombres = fields.One2many('upoferia.artista_disciplina', 'artista_id', string='Disciplinas')

    @api.constrains('fCache_base')
    def _check_cache_base(self):
        for record in self:
            if record.fCache_base < 0:
                raise ValidationError('«Caché base» no puede ser menor que 0.')

    @api.constrains('fPotencia_kw')
    def _check_fPotencia_kw(self):
        for record in self:
            if record.fPotencia_kw < 0:
                raise ValidationError('«Potencia (kW)» no puede ser menor que 0.')

    @api.constrains('sMontaje', 'sIluminacion', 'sSonido', 'sEspacio')
    def _check_longitud(self):
        for record in self:
            for campo in ('sMontaje', 'sIluminacion', 'sSonido', 'sEspacio'):
                if record[campo] and len(record[campo]) > 100:
                    raise ValidationError('«%s» no puede superar los 100 caracteres.' % record._fields[campo].string)

    @api.constrains('sMontaje', 'sIluminacion', 'sSonido', 'sEspacio')
    def _check_textos_opcionales(self):
        for record in self:
            for campo in ('sMontaje', 'sIluminacion', 'sSonido', 'sEspacio'):
                if record[campo] and not record[campo].strip():
                    raise ValidationError('«%s» no puede contener solo espacios.' % record._fields[campo].string)
