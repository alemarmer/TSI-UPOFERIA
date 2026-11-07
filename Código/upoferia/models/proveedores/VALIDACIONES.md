## CategoriaProveedor (`upoferia.categoria_proveedor`) — `categoria_proveedor.py`

### `sNombre` (Char) — clave
- Obligatorio — `required`
- Único — `_sql_constraints`
- No vacío ni solo espacios — `@api.constrains`
- Sin espacios al principio ni al final — `@api.constrains`
- Entre 2 y 50 caracteres — `@api.constrains`
- Único sin distinguir mayúsculas («Catering» = «CATERING») — `@api.constrains`

### `iColor` (Integer)
- Número entre 0 y 11 (la paleta de colores de las etiquetas de Odoo); por defecto 0 — `@api.constrains`

### Relaciones
- `padre_id` (Many2one → CategoriaProveedor) — opcional, relación reflexiva «es subcategoría de»; no se puede borrar una categoría que tenga subcategorías (`ondelete='restrict'`). Una categoría no puede ser su propia madre ni tener como madre a una de sus subcategorías (no forma ciclos) — `@api.constrains` con `_has_cycle`- `hija_ids` (One2many → CategoriaProveedor) — subcategorías (inverso de `padre_id`).
- `proveedor_ids` (Many2many → Proveedor) — relación «clasifica»; tabla intermedia `upoferia_proveedor_categoria_rel` (la PROVEEDOR_CATEGORIA del relacional).

## Proveedor (`upoferia.proveedor`) — `proveedor.py`

### `sCif` (Char)
- Único — `_sql_constraints`
- Una letra mayúscula, 7 dígitos y un carácter de control, sin espacios (ej. `B12345674`) — `@api.constrains`
- Carácter de control correcto según el algoritmo oficial del CIF — `@api.constrains`

### Relaciones
- `categoria_ids` (Many2many → CategoriaProveedor) — relación «clasifica»; misma tabla intermedia `upoferia_proveedor_categoria_rel`.
- `transaccion_ids` (One2many → Transaccion) — transacciones en las que interviene (inverso de `proveedor_id` en `compras/transaccion.py`).
- `marca_ids` (One2many → Marca) — marcas que comercializa (inverso de `proveedor_id` en `patrocinios/marca.py`).
- `servicio_proveedor_ids` (One2many → ServicioProveedor) — servicios que ofrece con su tarifa (inverso de `proveedor_id` en `patrocinios/servicio_proveedor.py`).

---

# Notas sobre la documentación

Los diagramas (E-R, relacional y UML) mantienen los nombres originales de los atributos (`nombre`, `color`, `cif`). En el código llevan la notación húngara (`sNombre`, `iColor`, `sCif`), pero de momento los diagramas no se cambian.

Nota: en el código los campos de relación siguen la convención de Odoo que usa el profesor (`_id` / `_ids`), mientras que el relacional usa los nombres de las claves ajenas (`dni_proveedor`, `codigo_tipo_transaccion`…). Las claves ajenas compuestas del relacional se convierten en un único Many2one, porque Odoo enlaza por su `id` interno. Igual que con la notación húngara, los diagramas no se cambian.

Nota: `proveedor.py` tiene relaciones inversas con modelos de compras (Transaccion) y de patrocinios (Marca, ServicioProveedor), así que las tres carpetas se tienen que cargar a la vez en Odoo.

---

# Pendiente de revisar


- **Herencia de Persona (pendiente).** Según el UML, Proveedor es subtipo de Persona (en Odoo, `_inherits`). `socios/persona.py` todavía está vacío.
- **Proveedor no tiene `_rec_name`.** En los desplegables (por ejemplo, al elegir el proveedor de una transacción o de una marca) aparecerá como «upoferia.proveedor,1». Se arreglará cuando herede de Persona y tenga nombre.
