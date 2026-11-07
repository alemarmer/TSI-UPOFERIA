from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Material(models.Model):

    _name = "upoferia.material"
    _description = "Material"
    _rec_name = "nombre"
    _rec_names_search = ["codigo_interno", "nombre"]
    _order = "codigo_interno"

    codigo_interno = fields.Char(
        string="Código interno", required=True, help="Identificador único del material"
    )
    nombre = fields.Char(string="Nombre", required=True)
    tipo_propiedad = fields.Selection(
        [
            ("fijo", "Fijo"),
            ("propio", "Propio"),
            ("alquilado", "Alquilado"),
        ],
        "Tipo de propiedad",
        required=True,
        default="propio",
    )
    cantidad_total = fields.Integer(string="Cantidad total", default=1)
    estado_conservacion = fields.Selection(
        [
            ("nuevo", "Nuevo"),
            ("bueno", "Bueno"),
            ("regular", "Regular"),
            ("deteriorado", "Deteriorado"),
        ],
        "Estado de conservación",
        default="bueno",
    )
    fecha_adquisicion = fields.Date(string="Fecha de adquisición")
    observaciones = fields.Text(string="Observaciones")

    # Relaciones
    categoria_material_id = fields.Many2one(
        "upoferia.categoria_material",
        string="Categoría",
        required=True,
        ondelete="restrict",
    )
    uso_material_ids = fields.One2many(
        "upoferia.uso_material", "material_id", string="Usos en tareas"
    )
    prestamo_linea_ids = fields.One2many(
        "upoferia.prestamo_linea", "material_id", string="Préstamos"
    )

    _sql_constraints = [
        (
            "codigo_interno_unique",
            "UNIQUE(codigo_interno)",
            "Ya existe un material con ese código interno.",
        ),
        (
            "cantidad_total_no_negativa",
            "CHECK(cantidad_total >= 0)",
            "La cantidad total no puede ser negativa.",
        ),
    ]

    @api.depends("codigo_interno", "nombre")
    def _compute_display_name(self):
        for record in self:
            record.display_name = "[%s] %s" % (
                record.codigo_interno or "",
                record.nombre or "",
            )

    @api.constrains("codigo_interno", "nombre")
    def _check_codigo_nombre(self):
        for record in self:
            if not record.codigo_interno.strip():
                raise ValidationError(
                    "El código interno del material no puede estar vacío."
                )
            if not record.nombre.strip():
                raise ValidationError("El nombre del material no puede estar vacío.")

    @api.onchange("cantidad_total")
    def onchange_cantidad_total(self):
        if self.cantidad_total == 0:
            return {
                "warning": {
                    "title": "Cantidad a cero",
                    "message": "El material tiene una cantidad total de 0. Comprueba que es correcto.",
                }
            }
