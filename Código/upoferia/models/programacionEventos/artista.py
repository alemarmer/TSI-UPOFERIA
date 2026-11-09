# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Artista(models.Model):
    _name = 'upoferia.artista'
    _description = 'Artista'
    _rec_name = 'sDni'

    #poner dni como FK
    sDni = fields.Char(string="DNI del artista", size=9, required=True)
    fCache_base = fields.Float(string='Caché base')
    sMontaje = fields.Char(string='Montaje')
    bIluminacion = fields.Boolean(string='Iluminación')
    fPotencia_kw = fields.Float(string='Potencia (kW)')
    sSonido = fields.Char(string='Sonido')
    sEspacio = fields.Char(string='Espacio')

    disciplina_ids = fields.One2many('upoferia.artista_disciplina', 'artista_id', string='Disciplinas')
    actuacion_ids = fields.Many2many('upoferia.actuacion', 'upoferia_actuacion_artista',
                                     'artista_id', 'actuacion_id', string='Actuaciones')

    _sql_constraints = [('artista_sDni_unique', 'UNIQUE ("sDni")', 'Ya existe un artista con ese DNI.')]

    def unlink(self):
        for record in self:
            if record.disciplina_ids:
                raise models.ValidationError('No se puede borrar un artista que tiene disciplinas. Borra primero sus disciplinas.')
        return super(Artista, self).unlink()

    @api.constrains('fCache_base', 'fPotencia_kw')
    def _check_valores(self):
        for record in self:
            if record.fCache_base < 0:
                raise models.ValidationError('El caché base no puede ser negativo.')
            if record.fPotencia_kw < 0:
                raise models.ValidationError('La potencia no puede ser negativa.')

    @api.constrains('sMontaje', 'sSonido', 'sEspacio')
    def _check_textos(self):
        for record in self:
            if record.sMontaje and not record.sMontaje.strip():
                raise models.ValidationError('El montaje no puede contener solo espacios.')
            if record.sSonido and not record.sSonido.strip():
                raise models.ValidationError('El sonido no puede contener solo espacios.')
            if record.sEspacio and not record.sEspacio.strip():
                raise models.ValidationError('El espacio no puede contener solo espacios.')

    @api.constrains('sMontaje', 'sSonido', 'sEspacio')
    def _check_longitud(self):
        for record in self:
            if record.sMontaje and len(record.sMontaje) > 100:
                raise models.ValidationError('El montaje no puede superar los 100 caracteres.')
            if record.sSonido and len(record.sSonido) > 100:
                raise models.ValidationError('El sonido no puede superar los 100 caracteres.')
            if record.sEspacio and len(record.sEspacio) > 100:
                raise models.ValidationError('El espacio no puede superar los 100 caracteres.')
