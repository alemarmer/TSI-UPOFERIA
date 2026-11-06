from odoo import models, fields, api

class PuntoAcceso(models.Model):
    _name = 'upoferia.control_accesos.punto_acceso'
    _description = 'Punto de acceso'

    name = fields.Char("Nombre", required=True)
    ip_dispositivo = fields.Char("IP del dispositivo")
    tipo_dispositivo = fields.Char("Tipo de dispositivo")
    nombre_case = fields.Char("Nombre de la caseta")
    nombre_zona_caseta = fields.Char("Nombre de la zona de la caseta")
    registro_accesos_ids = fields.One2many('upoferia.control_accesos.registro_accesos', 'punto_acceso_id', string="Registros de accesos")
    