# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Tipo_evento(models.Model):
    _name = 'upoferia.tipo_evento'
    _description = 'Tipo de evento'
    _rec_name = 'sNombre_tipo_evento'

    sNombre_tipo_evento = fields.Char(string="Nombre del tipo de evento", required=True)
    sDescripcion = fields.Text(string="Descripción del tipo de evento")

    evento_ids = fields.One2many('upoferia.evento', 'tipo_evento_id', string='Eventos')

    _sql_constraints = [('tipo_evento_sNombre_unique', 'UNIQUE ("sNombre_tipo_evento")', 'Ya existe un tipo de evento con ese nombre.')]

    @api.constrains('sNombre_tipo_evento', 'sDescripcion')
    def _check_textos(self):
        for record in self:
            if not record.sNombre_tipo_evento.strip():
                raise models.ValidationError('El nombre del tipo de evento es obligatorio.')
            if record.sDescripcion and not record.sDescripcion.strip():
                raise models.ValidationError('La descripción no puede contener solo espacios.')

    @api.constrains('sNombre_tipo_evento')
    def _check_longitud(self):
        for record in self:
            if record.sNombre_tipo_evento and len(record.sNombre_tipo_evento) > 100:
                raise models.ValidationError('El nombre del tipo de evento no puede superar los 100 caracteres.')
