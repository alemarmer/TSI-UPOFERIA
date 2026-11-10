from odoo import models, fields, api
class TipoSocio(models.Model):
    _name = 'upoferia.socios.tipo_socio'
    _description = 'Tipo de socio'

    name = fields.Char("Nombre", required=True)
    multiplicador_xp = fields.Float("Multiplicador de XP")
    cuota = fields.Float("Cuota mensual")
    num_beneficiarios = fields.Integer("Número máximo de beneficiarios")
    num_invitciones = fields.Integer("Número máximo de invitaciones")
    limite_credito = fields.Float("Límite de crédito")
    
    socio_ids = fields.One2many('upoferia.socios.socio', 'tipo_socio_id', string="Socios")
    
    @api.constrains('multiplicador_xp')
    def _check_multiplicador_xp(self):
        if self.multiplicador_xp < 0:
            raise models.ValidationError('El multiplicador de XP no puede ser negativo.')
    @api.constrains('cuota')
    def _check_cuota(self):
        if self.cuota < 0:
            raise models.ValidationError('La cuota no puede ser negativa.')
        
    @api.constrains('num_beneficiarios')
    def _check_num_beneficiarios(self):
        if self.num_beneficiarios < 0:
            raise models.ValidationError('El número de beneficiarios no puede ser negativo.')
        
    @api.constrains('num_invitciones')
    def _check_num_invitciones(self):
        if self.num_invitciones < 0:
            raise models.ValidationError('El número de invitaciones no puede ser negativo.')
        
    @api.constrains('limite_credito')
    def _check_limite_credito(self):
        if self.limite_credito < 0:
            raise models.ValidationError('El límite de crédito no puede ser negativo.')