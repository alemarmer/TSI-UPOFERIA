import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ExhibicionMarca(models.Model):
    _name = 'upoferia.exhibicion_marca'
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

    marca_id = fields.Many2one('upoferia.marca', string='Marca', required=True, ondelete='restrict')
    tecnico_id = fields.Many2one('upoferia.tecnico', string='Técnico', ondelete='set null')
    espacio_publicitario_id = fields.Many2one('upoferia.espacio_publicitario', string='Espacio publicitario', required=True, ondelete='restrict')

    sEstadoExhibicion = fields.Selection([
        ('sin_programar', 'Sin programar'),
        ('programada', 'Programada'),
        ('montada', 'Montada'),
        ('retirada', 'Retirada'),
    ], string='Estado', compute='_compute_estadoExhibicion')

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

    @api.constrains('dFechaMontaje', 'dFechaRetirada', 'espacio_publicitario_id')
    def _check_solapamiento(self):
        oRegistro = None
        lDominio = []
        oOtra = None
        sRetiradaOtra = ''
        for oRegistro in self:
            if not oRegistro.dFechaMontaje:
                continue
            lDominio = [
                ('id', '!=', oRegistro.id),
                ('espacio_publicitario_id', '=', oRegistro.espacio_publicitario_id.id),
                ('dFechaMontaje', '!=', False),
                '|', ('dFechaRetirada', '=', False), ('dFechaRetirada', '>=', oRegistro.dFechaMontaje),
            ]
            if oRegistro.dFechaRetirada:
                lDominio.append(('dFechaMontaje', '<=', oRegistro.dFechaRetirada))
            oOtra = self.search(lDominio, limit=1)
            if oOtra:
                sRetiradaOtra = oOtra.dFechaRetirada.strftime('%d/%m/%Y') if oOtra.dFechaRetirada else 'sin fecha de retirada'
                raise ValidationError('El espacio publicitario «%s» ya está ocupado por la exhibición «%s» (del %s al %s).' % (
                    oRegistro.espacio_publicitario_id.sCodigoLugar,
                    oOtra.sIdExhibicion,
                    oOtra.dFechaMontaje.strftime('%d/%m/%Y'),
                    sRetiradaOtra,
                ))

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

    @api.depends('dFechaMontaje', 'dFechaRetirada')
    def _compute_estadoExhibicion(self):
        oRegistro = None
        dHoy = fields.Date.context_today(self)
        for oRegistro in self:
            if not oRegistro.dFechaMontaje:
                oRegistro.sEstadoExhibicion = 'sin_programar'
            elif dHoy < oRegistro.dFechaMontaje:
                oRegistro.sEstadoExhibicion = 'programada'
            elif not oRegistro.dFechaRetirada or dHoy <= oRegistro.dFechaRetirada:
                oRegistro.sEstadoExhibicion = 'montada'
            else:
                oRegistro.sEstadoExhibicion = 'retirada'