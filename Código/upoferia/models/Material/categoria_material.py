from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CategoriaMaterial(models.Model):

    _name = "upoferia.categoria_material"
    _description = "Categoría de material"
    _rec_name = "sNombre"
    _order = "sNombre"

    sNombre = fields.Char(
        string="Nombre",
        required=True,
        help="Identificador único de la categoría de material",
    )
    # Relaciones
    padre_id = fields.Many2one(
        "upoferia.categoria_material", string="Categoría padre"
    )
    hijo_ids = fields.One2many(
        "upoferia.categoria_material", "padre_id", string="Subcategorías"
    )
    material_ids = fields.One2many(
        "upoferia.material", "categoria_material_id", string="Materiales"
    )

    _sql_constraints = [
        (
            "nombre_unique",
            'UNIQUE("sNombre")',
            "Ya existe una categoría de material con ese nombre.",
        ),
    ]

    @api.constrains("sNombre")
    def _check_nombre(self):
        for record in self:
            if not record.sNombre.strip():
                raise ValidationError(
                    "El nombre de la categoría de material no puede estar vacío."
                )

    @api.constrains("padre_id")
    def _check_padre(self):
        for record in self:
            visitados = {record.id}
            padre = record.padre_id
            while padre:
                if padre.id in visitados:
                    raise ValidationError(
                        "Una categoría no puede ser subcategoría de sí misma ni formar ciclos."
                    )
                visitados.add(padre.id)
                padre = padre.padre_id
