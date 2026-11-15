from odoo import models, fields, api

class RegistroAccesos(models.Model):
    _name = 'upoferia.control_accesos.registro_accesos'
    _description = 'Registro de accesos'
    _rec_name = 'id'

    punto_acceso_id = fields.Many2one('upoferia.control_accesos.punto_acceso', string='Punto de acceso', required=True, ondelete='cascade')
    fecha_hora = fields.Datetime("Fecha y hora de acceso",default=fields.Datetime.now)
    metodo_acceso = fields.Selection( selection=[('facial', 'Patrón Facial'), ('qr', 'Escáner de QR'), ('manual', 'Entrada manual'),],string="Metodo de acceso")
    tipo_movimiento = fields.Selection( selection=[('entrada', 'Entrada a la caseta'), ('salida', 'Salida de la caseta'),],string="Tipo de movimiento")
    persona_id = fields.Many2one('upoferia.socios.persona', string='Persona', required=True, ondelete='cascade')
    evento_puerta_id = fields.Many2one('upoferia.control_accesos.evento_puerta', string='Evento de puerta', required=True, ondelete='cascade')
    
    def _error_con_incidencia(self, motivo):
            self.env['upoferia.control_accesos.incidencia_puerta'].create({ 
                'motivo': motivo
            })
            return {
                'ok': False,
                'message': motivo
            }
            
    @api.model
    def registrar_acceso_qr(self, codigo, punto_acceso_id):
        
        punto_acceso = self.env['upoferia.control_accesos.punto_acceso'].browse(punto_acceso_id)
        if not punto_acceso.exists():
            return self._error_con_incidencia('El punto de acceso no existe.')
        
        persona = self.env['upoferia.socios.persona'].search([('codigo_persona', '=', codigo)], limit=1)
        if not persona.exists():
            return self._error_con_incidencia('No se encontró ninguna persona con el código proporcionado.')
        
        tipo_movimiento = 'salida' if self.env['upoferia.control_accesos.registro_accesos'].search([
            ('punto_acceso_id.nombre_caseta', '=', punto_acceso.nombre_caseta), 
            ('persona_id', '=', persona.id)], 
            order='id desc', limit=1).tipo_movimiento == 'entrada' else 'entrada'
        
        aforo_actual = self.env['upoferia.control_accesos.control_aforo'].search([
            ('evento_puerta_id.registro_accesos_ids.punto_acceso_id.nombre_caseta', '=', punto_acceso.nombre_caseta)], order='id desc', limit=1)
        if not aforo_actual.exists():
            return self._error_con_incidencia('No se pueden registrar accesos. No hay registros de aforo para esta caseta.')
        
        if aforo_actual.aforo_actual >= aforo_actual.aforo_maximo and tipo_movimiento == 'entrada':
            return self._error_con_incidencia('No se puede registrar la entrada. El aforo máximo de la caseta ha sido alcanzado.')

        if aforo_actual.aforo_actual <= 0 and tipo_movimiento == 'salida':
            return self._error_con_incidencia('No se puede registrar la salida. La caseta está vacía.')
        
        aforo = self.env['upoferia.control_accesos.control_aforo'].create({
            'punto_acceso_id': punto_acceso_id,
            'aforo_actual': aforo_actual.aforo_actual + 1 if tipo_movimiento == 'entrada' else aforo_actual.aforo_actual - 1,
            'aforo_maximo': aforo_actual.aforo_maximo
            })
        
        self.create({
            'punto_acceso_id': punto_acceso_id,
            'persona_id': persona.id,
            'evento_puerta_id': aforo.evento_puerta_id.id,
            'fecha_hora': fields.Datetime.now(),
            'metodo_acceso': 'qr',
            'tipo_movimiento': tipo_movimiento
        })
        
        return {
            'ok': True,
            'nombre_persona': persona.nombre,
            'tipo_movimiento': tipo_movimiento,
            'aforo_actual': aforo.aforo_actual,
            'aforo_maximo': aforo.aforo_maximo,
            'message': f'Acceso registrado correctamente para {persona.nombre}. Aforo actual: {aforo.aforo_actual}/{aforo.aforo_maximo}.'
        } 
    
    