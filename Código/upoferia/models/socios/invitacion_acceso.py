from odoo import models, fields, api
class InvitacionAcceso(models.Model):
    _name = 'upoferia.socios.invitacion_acceso'
    _description = 'Invitación de acceso'

    name = fields.Char("DNI del socio",size=9, required=True)
    name2 = fields.Char("DNI del invitado",size=9, required=True)
    fecha_validez = fields.Date("Fecha de validez", autodate=True)