from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Patrocinio(models.Model):
    _name = 'upoferia.patrocinio'
    _description = 'Patrocinio de una marca a un evento'
    _sql_constraints = [
        ('marca_evento_uniq', 'UNIQUE ("marca_id", "evento_id")',
         'Esa marca ya patrocina ese evento.'),
    ]

    fImporteAportacion = fields.Float(string='Importe de la aportación')
    sTipoAportacion = fields.Selection([
        ('economica', 'Económica'),
        ('especie', 'En especie'),
    ], string='Tipo de aportación')

    marca_id = fields.Many2one('upoferia.marca', string='Marca', required=True, ondelete='cascade')
    evento_id = fields.Many2one('upoferia.evento', string='Evento', required=True, ondelete='cascade')

    @api.constrains('fImporteAportacion')
    def _check_importe_aportacion(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.fImporteAportacion < 0:
                raise ValidationError('«Importe de la aportación» no puede ser menor que 0.')
            if oRegistro.fImporteAportacion > 1000000:
                raise ValidationError('«Importe de la aportación» no puede superar 1.000.000 €.')
            if round(oRegistro.fImporteAportacion, 2) != oRegistro.fImporteAportacion:
                raise ValidationError('«Importe de la aportación» solo admite dos decimales (céntimos).')

    @api.depends('marca_id.sNombre', 'evento_id')
    def _compute_display_name(self):
        oRegistro = None
        for oRegistro in self:
            oRegistro.display_name = '%s → %s' % (oRegistro.marca_id.sNombre or '', oRegistro.evento_id.display_name or '')
