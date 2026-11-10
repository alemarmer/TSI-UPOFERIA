from odoo import models, fields, api
from datetime import timedelta


class TemporadaPase(models.Model):

    _name = 'upoferia.temporada_pase'
    _description = 'Temporada del pase de feria'
    _rec_name = 'nombre'

    nombre = fields.Char(string="Nombre", required=True, help="Nombre de la edición, por ejemplo «Feria 2026»")
    fecha_inicio = fields.Date(string="Fecha de inicio", required=True)
    fecha_fin = fields.Date(string="Fecha de fin", required=True)

    # Relaciones
    registro_xp_ids = fields.One2many('upoferia.registro_xp', 'temporada_pase_id', string="Registros de experiencia")
    clan_ids = fields.Many2many('upoferia.clan', 'upoferia_clan_temporada_pase_rel',
                                'temporada_pase_id', 'clan_id', string="Clanes participantes")

    _sql_constraints = [
        ('nombre_unique', 'UNIQUE(nombre)', 'Ya existe una temporada con ese nombre.'),
        ('fechas_orden', 'CHECK(fecha_fin >= fecha_inicio)', 'La fecha de fin no puede ser anterior a la de inicio.'),
    ]

    @api.constrains('nombre')
    def _check_nombre(self):
        for record in self:
            if not record.nombre.strip():
                raise models.ValidationError('El nombre de la temporada no puede estar vacío.')

    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_solapamiento(self):
        for record in self:
            solapada = self.search([('id', '!=', record.id),
                                    ('fecha_inicio', '<=', record.fecha_fin),
                                    ('fecha_fin', '>=', record.fecha_inicio)], limit=1)
            if solapada:
                raise models.ValidationError('La temporada se solapa con «%s».' % solapada.nombre)

    @api.onchange('fecha_inicio')
    def onchange_fecha_inicio(self):
        if self.fecha_inicio and not self.fecha_fin:
            self.fecha_fin = self.fecha_inicio + timedelta(days=30)