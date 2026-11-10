from odoo import models, fields, api

class RegistroAccesos(models.Model):
    _name = 'upoferia.control_accesos.registro_accesos'
    _description = 'Registro de accesos'
    _rec_name = 'id'

    punto_acceso_id = fields.Many2one('upoferia.control_accesos.punto_acceso', string='Punto de acceso', required=True, ondelete='cascade')
    fecha_hora = fields.Datetime("Fecha y hora de acceso",autodate=True)
    metodo_acceso = fields.Selection( selection=[('facial', 'Patrón Facial'), ('qr', 'Escáner de QR'), ('manual', 'Entrada manual'),],string="Metodo de acceso")
    tipo_movimiento = fields.Selection( selection=[('entrada', 'Entrada a la caseta'), ('salida', 'Salida de la caseta'),],string="Tipo de movimiento")
    persona_id = fields.Many2one('upoferia.socios.persona', string='Persona', required=True, ondelete='cascade')
    evento_puerta_id = fields.Many2one('upoferia.control_accesos.evento_puerta', string='Evento de puerta', required=True, ondelete='cascade')
    
