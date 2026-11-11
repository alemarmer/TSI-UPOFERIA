# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Caseta(models.Model):
    _name = 'upoferia.caseta'
    _description = 'Caseta'
    _rec_name = 'sNombre'

    sNombre = fields.Char(string='Nombre', required=True)
    sCalle = fields.Char(string='Calle')
    sNumero = fields.Char(string='Número')
    iModulos = fields.Integer(string='Módulos', required=True, default=1)
    iAforoAutorizado = fields.Integer(string='Aforo autorizado', required=True)
    fHoraApertura = fields.Float(string='Hora de apertura')
    fHoraCierre = fields.Float(string='Hora de cierre')

    zona_ids = fields.One2many('upoferia.zona_caseta', 'caseta_id', string='Zonas')
    mobiliario_ids = fields.One2many('upoferia.mobiliario_caseta', 'caseta_id', string='Mobiliario')
    licencia_ids = fields.One2many('upoferia.licencia', 'caseta_id', string='Licencias')
    inspeccion_ids = fields.One2many('upoferia.inspeccion', 'caseta_id', string='Inspecciones')

    _sql_constraints = [
                ('nombre_uniq', 'UNIQUE ("sNombre")',
                 'Ya existe una caseta con ese nombre.'),
    ]

    @api.constrains('iModulos', 'iAforoAutorizado')
    def _check_capacidad(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.iModulos <= 0:
                raise models.ValidationError('El número de «Módulos» de la caseta tiene que ser mayor que 0.')
            if oRegistro.iAforoAutorizado <= 0:
                raise models.ValidationError('El «Aforo autorizado» de la caseta tiene que ser mayor que 0.')

    def unlink(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.licencia_ids:
                raise models.UserError(f'No se puede borrar la caseta «{oRegistro.sNombre}» porque tiene licencias.')
            if oRegistro.inspeccion_ids:
                raise models.UserError(f'No se puede borrar la caseta «{oRegistro.sNombre}» porque tiene inspecciones.')
        self.zona_ids.unlink()
        self.mobiliario_ids.write({'caseta_id': False, 'dFechaAsignacion': False})
        return super().unlink()
