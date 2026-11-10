from odoo import models, fields, api

class EventoPuerta(models.Model):
    _name = 'upoferia.control_accesos.evento_puerta'
    _description = 'Evento de puerta'
    _rec_name = 'evento_puerta_num'

    evento_puerta_num = fields.Integer("ID del evento de puerta", readonly=True,default=0)
    registro_accesos_ids = fields.One2many('upoferia.control_accesos.registro_accesos', 'evento_puerta_id', string='Registros de accesos')
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('evento_puerta_num'):
                ultimo_evento = self.search([], order='evento_puerta_num desc', limit=1)
                vals['evento_puerta_num'] = (ultimo_evento.evento_puerta_num + 1) if ultimo_evento else 1
        return super().create(vals_list)
    
    