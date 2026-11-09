# Validaciones — Proveedores

## CategoriaProveedor (`upoferia.categoria_proveedor`) — `categoria_proveedor.py`

### `sNombre` (Char) — clave
- Obligatorio y con entre 2 y 50 caracteres sin contar los espacios del principio y del final — `required` / `@api.constrains`
### `iColor` (Integer)
- Color de la etiqueta (0 a 11, los colores de Odoo); en la vista se elige con `widget="color_picker"`.

### Relaciones
- `padre_id` (Many2one → CategoriaProveedor) — opcional, relación reflexiva «es subcategoría de». Si se borra una categoría, sus subcategorías se quedan sin madre. Una categoría no puede ser su propia madre ni tener como madre a una de sus subcategorías (no forma ciclos) — `@api.constrains` (se sube de padre en padre y, si se vuelve a la misma categoría, da error)
- `hija_ids` (One2many → CategoriaProveedor) — subcategorías (inverso de `padre_id`).
- `proveedor_ids` (Many2many → Proveedor) — tabla `upoferia_proveedor_categoria_rel`.

## Proveedor (`upoferia.proveedor`) — `proveedor.py`

### Herencia
- Proveedor es subtipo de Persona (en el relacional su clave `dni` es clave ajena de PERSONA): hereda sus campos (nombre, DNI, teléfono…) con `_inherits = {'upoferia.persona': 'persona_id'}`, como en el ejemplo del Tema 5.
- En los desplegables aparece con el nombre de su persona (`_rec_name = 'sNombre'`, el campo heredado de Persona).
- `persona_id` (Many2one → Persona) — obligatorio, con `ondelete='cascade'`, que Odoo exige para `_inherits`: si se borra el proveedor, se borra su persona.

### `sCif` (Char)
- Único — `_sql_constraints`
- Si se rellena, tiene 9 caracteres — `@api.constrains`

### Relaciones
- `transaccion_ids` (One2many → Transaccion) — transacciones del proveedor.
- `categoria_ids` (Many2many → CategoriaProveedor) — misma tabla que `proveedor_ids` de la categoría.
- `marca_ids` (One2many → Marca) — marcas que comercializa.
- `servicio_proveedor_ids` (One2many → ServicioProveedor) — servicios que ofrece, con su tarifa.
- `prestamo_ids` (One2many → Prestamo) — inverso de `proveedor_id` en Prestamo.
- Botón «Eliminar tarifas» (`btn_eliminarTarifas`): borra las tarifas del proveedor con la tupla `(2, id)`. Hace falta para poder borrarlo.

---

# Notas sobre la documentación

Los diagramas mantienen los nombres originales de los atributos (`nombre`, `color`, `cif`). En el código llevan la notación húngara (`sNombre`, `iColor`, `sCif`).

Nota: los campos de relación siguen la convención de Odoo (`_id` / `_ids`), porque Odoo enlaza por su `id` interno.

Nota: las relaciones no llevan `ondelete` (salvo `persona_id`, que lo exige `_inherits`), así que Odoo aplica su comportamiento por defecto: si el Many2one es obligatorio no deja borrar el registro al que apunta, y si es opcional lo borra y deja el campo vacío. Para poder borrar un registro que tiene otros que dependen de él, se usan los botones `btn_eliminar...`, que borran antes esos registros con `write` y la tupla `(2, id)`, como se vio en el Tema 6_2.

---

# Pendiente de revisar

- **Nombres que deben usar los compañeros.** Se supone que existen `upoferia.persona` (con su nombre en el campo `sNombre`) y `upoferia.prestamo` (este con un Many2one `proveedor_id`). Hasta que estén en la rama, el módulo no se instala.
