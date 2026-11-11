# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Inspeccion(models.Model):
    _name = 'upoferia.inspeccion'
    _description = 'Inspección'
    _rec_name = 'sReferencia'
    _sql_constraints = [
        ('referencia_uniq', 'UNIQUE ("sReferencia")',
         'Ya existe una inspección con esa referencia.'),
    ]

    sReferencia = fields.Char(string='Referencia', required=True)
    sTipo = fields.Selection([
        ('seguridad', 'Seguridad e incendios'),
        ('electrica', 'Instalación eléctrica'),
        ('estructural', 'Estructura y montaje'),
        ('sanitaria', 'Sanitaria'),
        ('aforo', 'Aforo'),
        ('veterinaria', 'Veterinaria'),
    ], string='Tipo', required=True)
    sOrganismo = fields.Char(string='Organismo')
    dFecha = fields.Date(string='Fecha', required=True)
    sResultado = fields.Selection([
        ('favorable', 'Favorable'),
        ('favorable_condiciones', 'Favorable con condiciones'),
        ('desfavorable', 'Desfavorable'),
    ], string='Resultado')
    sDocumento = fields.Char(string='Documento')
    sEstado = fields.Selection([
        ('programada', 'Programada'),
        ('realizada', 'Realizada'),
        ('cancelada', 'Cancelada'),
    ], string='Estado', required=True, default='programada')

    caseta_id = fields.Many2one('upoferia.caseta', string='Caseta', required=True)
    punto_control_ids = fields.One2many('upoferia.punto_control', 'inspeccion_id', string='Puntos de control')
    inspeccion_inspector_ids = fields.One2many('upoferia.inspeccion_inspector', 'inspeccion_id', string='Inspectores')

    fPorcentajeSuperado = fields.Float(string='Porcentaje superado (%)', compute='_compute_porcentaje_superado', store=True)

    @api.depends('punto_control_ids', 'punto_control_ids.sResultado')
    def _compute_porcentaje_superado(self):
        oRegistro = None
        iTotal = 0
        iSuperados = 0
        for oRegistro in self:
            iTotal = len(oRegistro.punto_control_ids)
            iSuperados = len(oRegistro.punto_control_ids.filtered(lambda oPunto: oPunto.sResultado == 'superado'))
            oRegistro.fPorcentajeSuperado = round(iSuperados / iTotal * 100, 2) if iTotal else 0.0

    @api.constrains('sEstado', 'sResultado')
    def _check_estado(self):
        oRegistro = None
        for oRegistro in self:
            if oRegistro.sEstado == 'realizada' and not oRegistro.sResultado:
                raise models.ValidationError('Una inspección realizada tiene que tener «Resultado».')

    def unlink(self):
        self.punto_control_ids.unlink()
        self.inspeccion_inspector_ids.unlink()
        return super().unlink()
