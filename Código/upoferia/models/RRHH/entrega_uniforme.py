# Autor: Juanjo (Personal - RRHH y Turnos)
from odoo import models, fields, api
import re

TALLAS = ('XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL')


class EntregaUniforme(models.Model):

    _name = 'upoferia.rrhh.entrega_uniforme'
    _description = 'Entrega de uniforme a un empleado'
    _rec_names_search = ['empleado_id', 'prenda']
    _order = 'fecha_entrega desc'

    fecha_entrega = fields.Date(string="Fecha de entrega", required=True, default=fields.Date.context_today)
    prenda = fields.Char(string="Prenda", size=100, required=True)
    talla = fields.Char(string="Talla", size=10, help="XS, S, M, L, XL, XXL o numérica (34-60)")
    cantidad = fields.Integer(string="Cantidad", default=1)
    estado = fields.Selection([('entregado', 'Entregado'),
                               ('devuelto', 'Devuelto'),
                               ('perdido', 'Perdido'),
                               ('deteriorado', 'Deteriorado'),],
                              'Estado', default='entregado')
    fecha_devolucion = fields.Date(string="Fecha de devolución")

    # Relaciones
    empleado_id = fields.Many2one('upoferia.rrhh.empleado', string="Empleado", required=True, ondelete='cascade')

    _sql_constraints = [
        ('natural_unique', 'UNIQUE(empleado_id, fecha_entrega, prenda)', 'Ese empleado ya recibió esa prenda en esa fecha.'),
        ('cantidad_check', 'CHECK(cantidad > 0)', 'La cantidad debe ser mayor que 0 (RN-68).'),
        ('fechas_check', 'CHECK(fecha_devolucion IS NULL OR fecha_devolucion >= fecha_entrega)',
         'La fecha de devolución no puede ser anterior a la de entrega (RN-68).'),
    ]

    @api.depends('empleado_id.nombre', 'prenda', 'fecha_entrega')
    def _compute_display_name(self):
        for record in self:
            record.display_name = '%s – %s (%s)' % (record.empleado_id.nombre or '?', record.prenda or '?', record.fecha_entrega or '')

    # Validaciones
    @api.constrains('prenda')
    def _check_prenda(self):
        for record in self:
            if not record.prenda.strip():
                raise models.ValidationError('La prenda no puede estar vacía.')

    @api.constrains('talla')
    def _check_talla(self):
        for record in self:
            if record.talla:
                t = record.talla.strip().upper()
                if t not in TALLAS and not (re.fullmatch(r'\d{2}', t) and 34 <= int(t) <= 60):
                    raise models.ValidationError('La talla «%s» no es válida. Usa XS, S, M, L, XL, XXL, XXXL o un número entre 34 y 60.'
                                          % record.talla)

    @api.constrains('estado', 'fecha_devolucion')
    def _check_estado_devolucion(self):
        for record in self:
            if record.estado == 'devuelto' and not record.fecha_devolucion:
                raise models.ValidationError('Una entrega «Devuelta» debe indicar la fecha de devolución.')
            if record.estado == 'entregado' and record.fecha_devolucion:
                raise models.ValidationError('Una entrega con fecha de devolución no puede seguir en estado «Entregado».')

    @api.constrains('fecha_entrega')
    def _check_fecha_entrega(self):
        hoy = fields.Date.context_today(self)
        for record in self:
            if record.fecha_entrega > hoy:
                raise models.ValidationError('La fecha de entrega no puede ser futura.')

    @api.constrains('cantidad')
    def _check_cantidad_maxima(self):
        for record in self:
            if record.cantidad > 10:
                raise models.ValidationError('No se pueden entregar más de 10 unidades de una prenda a la vez.')

    @api.onchange('fecha_devolucion')
    def onchange_fecha_devolucion(self):
        if self.fecha_devolucion and self.estado == 'entregado':
            self.estado = 'devuelto'

    @api.onchange('estado')
    def onchange_estado(self):
        if self.estado == 'devuelto' and not self.fecha_devolucion:
            self.fecha_devolucion = fields.Date.context_today(self)
        elif self.estado == 'entregado':
            self.fecha_devolucion = False

    @api.onchange('cantidad')
    def onchange_cantidad(self):
        if self.cantidad is not False and self.cantidad < 1:
            self.cantidad = 1
            return {
                'warning': {'title': 'Cantidad incorrecta', 'message': 'La cantidad mínima es 1.'}
            }

    # Reglas de negocio (capa ORM)
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if 'estado' in fields_list:
            res['estado'] = 'entregado'
        return res

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('talla'):
                vals['talla'] = vals['talla'].strip().upper()
            if vals.get('prenda'):
                vals['prenda'] = vals['prenda'].strip().capitalize()
            if vals.get('fecha_devolucion') and vals.get('estado', 'entregado') == 'entregado':
                vals['estado'] = 'devuelto'
        return super().create(vals_list)

    def write(self, vals):
        if vals.get('talla'):
            vals['talla'] = vals['talla'].strip().upper()
        if vals.get('prenda'):
            vals['prenda'] = vals['prenda'].strip().capitalize()
        if vals.get('fecha_devolucion') and 'estado' not in vals:
            # Solo pasa a «Devuelto» lo que estaba entregado (no lo perdido o deteriorado)
            entregadas = self.filtered(lambda r: r.estado == 'entregado')
            if entregadas:
                super(EntregaUniforme, entregadas).write(dict(vals, estado='devuelto'))
            return super(EntregaUniforme, self - entregadas).write(vals)
        return super().write(vals)

    def unlink(self):
        for record in self:
            if record.estado == 'entregado':
                raise models.UserError('No se puede eliminar una entrega pendiente de devolución (%s).' % record.display_name)
        return super().unlink()

    def copy(self, default=None):
        default = dict(default or {})
        default.update({'fecha_entrega': fields.Date.context_today(self), 'estado': 'entregado', 'fecha_devolucion': False})
        return super().copy(default)

    def action_registrar_devolucion(self):
        hoy = fields.Date.context_today(self)
        for record in self:
            record.write({'estado': 'devuelto', 'fecha_devolucion': max(hoy, record.fecha_entrega)})