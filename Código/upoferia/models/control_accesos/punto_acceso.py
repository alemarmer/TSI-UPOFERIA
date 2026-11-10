import re
from odoo import models, fields, api

class PuntoAcceso(models.Model):
    _name = 'upoferia.control_accesos.punto_acceso'
    _description = 'Punto de acceso'

    name = fields.Char("Nombre", required=True)
    ip_dispositivo = fields.Char("IP del dispositivo")
    tipo_dispositivo = fields.Selection(selection=[('camara', 'Cámara'), ('lector', 'Lector de tarjetas'), ('puerta', 'Puerta')], string="Tipo de dispositivo")
    nombre_case = fields.Char("Nombre de la caseta")
    nombre_zona_caseta = fields.Char("Nombre de la zona de la caseta")
    registro_accesos_ids = fields.One2many('upoferia.control_accesos.registro_accesos', 'punto_acceso_id', string="Registros de accesos")
    
    @api.constrains('ip_dispositivo')
    def _check_ip_dispositivo(self):
        if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", self.ip_dispositivo) is None:
            raise models.ValidationError('La IP del dispositivo no es válida.')