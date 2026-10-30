import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Servicio(models.Model):
    _name = 'feria.servicio'
    _description = 'Servicio'
    _rec_name = 'sCodigo'
    _sql_constraints = [
        ('codigo_uniq', 'UNIQUE ("sCodigo")',
         'Ya existe un servicio con ese código.'),
    ]

    sCodigo = fields.Char(string='Código', required=True)
    sUnidadFacturacion = fields.Char(string='Unidad de facturación')
    bRequiereTecnico = fields.Boolean(string='Requiere técnico')
    sNombre = fields.Char(string='Nombre', required=True)

    @api.constrains('sCodigo')
    def _check_codigo(self):
        oRegistro = None
        sCodigo = ''
        for oRegistro in self:
            sCodigo = oRegistro.sCodigo or ''
            if not sCodigo.strip():
                raise ValidationError('El campo «Código» es obligatorio.')
            if not 2 <= len(sCodigo) <= 20:
                raise ValidationError('El «Código» del servicio debe tener entre 2 y 20 caracteres.')
            if not re.fullmatch(r'[A-Z0-9]+([-/._][A-Z0-9]+)*', sCodigo):
                raise ValidationError('El «Código» del servicio solo puede tener letras mayúsculas y números, separados por - / . _ y sin espacios (por ejemplo SRV-SONIDO).')

    @api.constrains('sNombre')
    def _check_nombre(self):
        oRegistro = None
        sNombre = ''
        for oRegistro in self:
            sNombre = oRegistro.sNombre or ''
            if not sNombre.strip():
                raise ValidationError('El campo «Nombre» del servicio es obligatorio.')
            if sNombre != sNombre.strip():
                raise ValidationError('El nombre del servicio no puede empezar ni terminar con espacios.')
            if not 2 <= len(sNombre) <= 100:
                raise ValidationError('El nombre del servicio debe tener entre 2 y 100 caracteres.')

    @api.constrains('sUnidadFacturacion')
    def _check_unidad_facturacion(self):
        oRegistro = None
        sUnidad = ''
        for oRegistro in self:
            sUnidad = oRegistro.sUnidadFacturacion or ''
            if not sUnidad:
                continue
            if sUnidad != sUnidad.strip() or '  ' in sUnidad:
                raise ValidationError('La «Unidad de facturación» no puede empezar ni terminar con espacios ni tener dos espacios seguidos.')
            if not 2 <= len(sUnidad) <= 30:
                raise ValidationError('La «Unidad de facturación» debe tener entre 2 y 30 caracteres.')
