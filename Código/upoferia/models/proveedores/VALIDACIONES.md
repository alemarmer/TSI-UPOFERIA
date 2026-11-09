# Validaciones — Proveedores

## CategoriaProveedor (`upoferia.categoria_proveedor`) — `categoria_proveedor.py`

### `sNombre` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`

### `iColor` (Integer)
- Color de la etiqueta (0 a 11, los colores de Odoo); en la vista se elige con `widget="color_picker"`.

### Relaciones
- `padre_id` (Many2one → CategoriaProveedor) — opcional, relación reflexiva «es subcategoría de» (`ondelete='restrict'`). Una categoría no puede ser su propia madre ni tener como madre a una de sus subcategorías (no forma ciclos) — `@api.constrains` con `_has_cycle`
- `hija_ids` (One2many → CategoriaProveedor) — subcategorías (inverso de `padre_id`).
- `proveedor_ids` (Many2many → Proveedor) — tabla `upoferia_proveedor_categoria_rel`.

## Proveedor (`upoferia.proveedor`) — `proveedor.py`

### `sCif` (Char)
- Único — `_sql_constraints`
- Si se rellena, tiene 9 caracteres — `@api.constrains`

### Relaciones
- `transaccion_ids` (One2many → Transaccion) — transacciones del proveedor.
- `categoria_ids` (Many2many → CategoriaProveedor) — misma tabla que `proveedor_ids` de la categoría.
- `marca_ids` (One2many → Marca) — marcas que comercializa.
- `servicio_proveedor_ids` (One2many → ServicioProveedor) — servicios que ofrece, con su tarifa.

---

# Notas sobre la documentación

Los diagramas mantienen los nombres originales de los atributos (`nombre`, `color`, `cif`). En el código llevan la notación húngara (`sNombre`, `iColor`, `sCif`).

Nota: los campos de relación siguen la convención de Odoo (`_id` / `_ids`), porque Odoo enlaza por su `id` interno.

---

# Pendiente de revisar

- **Herencia de Persona.** Según el UML, Proveedor es subtipo de Persona (`_inherits`). Hasta entonces no tiene nombre y en los desplegables aparece como «upoferia.proveedor,1».
