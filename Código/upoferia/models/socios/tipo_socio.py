from odoo import models, fields, api
class TipoSocio(models.Model):
    _name = 'upoferia.tipo_socio'
    _description = 'Tipo de socio'

    nombre = fields.Char("Nombre", required=True)
    multiplicador_xp = fields.Float("Multiplicador de XP")
    cuota = fields.Float("Cuota mensual")
    num_beneficiarios = fields.Integer("Número máximo de beneficiarios")
    num_invitciones = fields.Integer("Número máximo de invitaciones")
    limite_credito = fields.Float("Límite de crédito")