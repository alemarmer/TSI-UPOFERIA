import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ExhibicionMarca(models.Model):
    _name = 'feria.exhibicion_marca'
    _description = 'Exhibición de marca'
    _rec_name = 'sIdExhibicion'
    _sql_constraints = [
        ('id_exhibicion_uniq', 'UNIQUE ("sIdExhibicion")',
         'Ya existe una exhibición con ese identificador.'),
    ]

    sIdExhibicion = fields.Char(string='Id. exhibición', required=True)
    dFechaMontaje = fields.Date(string='Fecha de montaje')
    sArteFinal = fields.Char(string='Arte final')
    dFechaRetirada = fields.Date(string='Fecha de retirada')

    @api.constrains('sIdExhibicion')
    def _check_id_exhibicion(self):
        oRegistro = None
        sId = ''
        for oRegistro in self:
            sId = oRegistro.sIdExhibicion or ''
            if not sId.strip():
                raise ValidationError('El campo «Id. exhibición» es obligatorio.')
            if not 2 <= len(sId) <= 20:
                raise ValidationError('El «Id. exhibición» debe tener entre 2 y 20 caracteres.')
            if not re.fullmatch(r'[A-Z0-9]+([-/._][A-Z0-9]+)*', sId):
                raise ValidationError('El «Id. exhibición» solo puede tener letras mayúsculas y números, separados por - / . _ y sin espacios (por ejemplo EXH-2026-01).')

    @api.constrains('dFechaMontaje')
    def _check_fecha_montaje(self):
        oRegistro = None
        dHoy = fields.Date.context_today(self)
        dFechaMinima = fields.Date.to_date('1970-01-01')
        for oRegistro in self:
            if not oRegistro.dFechaMontaje:
                continue
            if oRegistro.dFechaMontaje < dFechaMinima:
                raise ValidationError('La «Fecha de montaje» no puede ser anterior al 01/01/1970.')
            if (oRegistro.dFechaMontaje - dHoy).days > 730:
                raise ValidationError('La «Fecha de montaje» no puede ser más de dos años posterior a hoy.')

    @api.constrains('dFechaMontaje', 'dFechaRetirada')
    def _check_fecha_retirada(self):
        oRegistro = None
        for oRegistro in self:
            if not oRegistro.dFechaRetirada:
                continue
            if not oRegistro.dFechaMontaje:
                raise ValidationError('No se puede indicar la «Fecha de retirada» sin la «Fecha de montaje».')
            if oRegistro.dFechaRetirada < oRegistro.dFechaMontaje:
                raise ValidationError('«Fecha de retirada» no puede ser anterior a «Fecha de montaje».')
            if (oRegistro.dFechaRetirada - oRegistro.dFechaMontaje).days > 365:
                raise ValidationError('Una exhibición no puede durar más de un año entre el montaje y la retirada.')

    @api.constrains('sArteFinal')
    def _check_arte_final(self):
        oRegistro = None
        sArte = ''
        for oRegistro in self:
            sArte = oRegistro.sArteFinal or ''
            if not sArte:
                continue
            if not sArte.strip():
                raise ValidationError('El «Arte final» no puede estar formado solo por espacios.')
            if len(sArte) > 255:
                raise ValidationError('El «Arte final» no puede tener más de 255 caracteres.')
            if ' ' in sArte:
                raise ValidationError('El «Arte final» es una URL o una ruta de archivo y no puede tener espacios.')
            if not re.fullmatch(
                    r'(?i)https?://\S+|\S+\.(pdf|png|jpe?g|svg|ai|eps|tiff?)',
                    sArte):
                raise ValidationError('El «Arte final» debe ser una URL que empiece por http:// o https://, o un archivo .pdf, .png, .jpg, .jpeg, .svg, .ai, .eps, .tif o .tiff.')

    @api.onchange('dFechaMontaje', 'dFechaRetirada')
    def _onchange_valores(self):
        sMensaje = False
        if self.dFechaMontaje and self.dFechaRetirada and self.dFechaRetirada < self.dFechaMontaje:
            sMensaje = '«Fecha de retirada» no puede ser anterior a «Fecha de montaje».'
        if sMensaje:
            return {
                'warning': {
                    'title': 'Valores incorrectos',
                    'message': sMensaje,
                }
            }
