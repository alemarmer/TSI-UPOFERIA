from odoo import models, fields, api
class InvitacionAcceso(models.Model):
    _name = 'upoferia.socios.invitacion_acceso'
    _description = 'Invitación de acceso'

    socio_dni = fields.Char("DNI del socio",9, required=True)
    invitado_dni = fields.Char("DNI del invitado",9, required=True)
    fecha_validez = fields.Date("Fecha de validez")