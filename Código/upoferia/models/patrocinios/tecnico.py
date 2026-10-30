import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Tecnico(models.Model):
    _name = 'feria.tecnico'
    _description = 'Técnico'
    _sql_constraints = [
        ('cod_carnet_profesional_uniq', 'UNIQUE ("sCodCarnetProfesional")',
         'Ya existe un técnico con ese código de carné profesional.'),
    ]

    sEspecialidad = fields.Selection([
        ('electricidad', 'Electricidad'),
        ('sonido', 'Sonido'),
        ('iluminacion', 'Iluminación'),
        ('montaje', 'Montaje y estructuras'),
        ('fontaneria', 'Fontanería'),
        ('climatizacion', 'Climatización'),
        ('gas', 'Gas'),
    ], string='Especialidad')
    dFechaCaducidadCarnet = fields.Date(string='Caducidad del carné')
    sCodCarnetProfesional = fields.Char(string='Código del carné profesional')

    @api.constrains('sCodCarnetProfesional')
    def _check_cod_carnet_profesional(self):
        oRegistro = None
        sCodigo = ''
        for oRegistro in self:
            sCodigo = oRegistro.sCodCarnetProfesional or ''
            if not sCodigo:
                continue
            if not 4 <= len(sCodigo) <= 20:
                raise ValidationError('El «Código del carné profesional» debe tener entre 4 y 20 caracteres.')
            if not re.fullmatch(r'[A-Z0-9]+([-/._][A-Z0-9]+)*', sCodigo):
                raise ValidationError('El «Código del carné profesional» solo puede tener letras mayúsculas y números, separados por - / . _ y sin espacios (por ejemplo ELEC-12345).')

    @api.constrains('dFechaCaducidadCarnet', 'sCodCarnetProfesional')
    def _check_fecha_caducidad_carnet(self):
        oRegistro = None
        dHoy = fields.Date.context_today(self)
        dFechaMinima = fields.Date.to_date('1970-01-01')
        for oRegistro in self:
            if not oRegistro.dFechaCaducidadCarnet:
                continue
            if not oRegistro.sCodCarnetProfesional:
                raise ValidationError('No se puede indicar la «Caducidad del carné» sin el «Código del carné profesional».')
            if oRegistro.dFechaCaducidadCarnet < dFechaMinima:
                raise ValidationError('La «Caducidad del carné» no puede ser anterior al 01/01/1970.')
            if (oRegistro.dFechaCaducidadCarnet - dHoy).days > 15 * 365:
                raise ValidationError('La «Caducidad del carné» no puede ser más de 15 años posterior a hoy.')

    @api.onchange('dFechaCaducidadCarnet')
    def _onchange_fecha_caducidad_carnet(self):
        dHoy = fields.Date.context_today(self)
        if self.dFechaCaducidadCarnet and self.dFechaCaducidadCarnet < dHoy:
            return {
                'warning': {
                    'title': 'Carné caducado',
                    'message': 'El carné profesional de este técnico ya está caducado.',
                }
            }
