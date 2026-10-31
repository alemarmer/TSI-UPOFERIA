from odoo import models, fields, api

class RegistroAccesos(models.Model):
    _name = 'upoferia.control_accesos.registro_accesos'
    _description = 'Registro de accesos'

    name = fields.Char("Nombre del punto de acceso", required=True)
    fecha_hora = fields.Datetime("Fecha y hora de acceso",autodate=True)
    metodo_acceso = fields.Selection( selection=[('facial', 'Patrón Facial'), ('qr', 'Escáner de QR'), ('manual', 'Entrada manual'),],string="Metodo de acceso")
    metodo_acceso = fields.Selection( selection=[('entrada', 'Entrada a la caseta'), ('salida', 'Salida de la caseta'),],string="Tipo de movimiento")
    dni_usuario = fields.Char("DNI del usuario")
    id_evento_puerta = fields.Integer("ID del evento de puerta")