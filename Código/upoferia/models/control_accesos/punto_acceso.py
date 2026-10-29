from odoo import models, fields, api

class PuntoAcceso(models.Model):
    _name = 'upoferia.control_accesos.punto_acceso'
    _description = 'Punto de acceso'

    nombre_entrada = fields.Char("Nombre", required=True)
    ip_dispositivo = fields.Char("IP del dispositivo")
    tipo_dispositivo = fields.Char("Tipo de dispositivo")
    nombre_case = fields.Char("Nombre de la caseta")
    nombre_zona_cas = fields.Char("Nombre de la zona de la caseta")
    