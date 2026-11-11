from odoo import models, fields, api

class Recompensa(models.Model):

    _name = 'upoferia.recompensa'
    _description = 'Recompensa del pase de feria'
    _rec_name = 'nombre'

    nombre = fields.Char(string="Nombre", required=True, help="Nombre único de la recompensa")
    descripcion = fields.Text(string="Descripción")
    nivel_requerido = fields.Integer(string="Nivel requerido", default=1,
                                     help="Nivel del pase que hay que alcanzar para obtenerla")

    # Relaciones
    registro_xp_ids = fields.Many2many('upoferia.registro_xp', 'upoferia_registro_xp_recompensa_rel',
                                       'recompensa_id', 'registro_xp_id', string="Pendiente de canjear en")

    _sql_constraints = [
        ('nombre_unique', 'UNIQUE(nombre)', 'Ya existe una recompensa con ese nombre.'),
        ('nivel_minimo', 'CHECK(nivel_requerido >= 1)', 'El nivel requerido debe ser al menos 1.'),
    ]

    @api.constrains('nombre')
    def _check_nombre(self):
        for record in self:
            if not record.nombre.strip():
                raise models.ValidationError('El nombre de la recompensa no puede estar vacío.')