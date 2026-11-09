# Validaciones — Patrocinios y servicios

## Marca (`upoferia.marca`) — `marca.py`

### `sNombre` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`

### Relaciones
- `proveedor_id` (Many2one → Proveedor) — opcional, relación «comercializa» (`ondelete='set null'`).
- `exhibicion_ids` (One2many → ExhibicionMarca) — exhibiciones de la marca.
- `patrocinio_ids` (One2many → Patrocinio) — eventos que patrocina.
- `producto_ids` (One2many → Producto de tesorería) — inverso de `marca_id` en Producto.

## Patrocinio (`upoferia.patrocinio`) — `patrocinio.py`

### `fImporteAportacion` (Float)
- No menor que 0 — `@api.constrains`

### Relaciones
- `marca_id` (Many2one → Marca) y `evento_id` (Many2one → Evento de eventos) — obligatorios; si se borra uno, se borra el patrocinio (`ondelete='cascade'`).
- La pareja marca + evento no se repite (clave doble del relacional) — `_sql_constraints`

### Nombre que se muestra
- Aparece como `Cruzcampo → Concierto inaugural` — `_compute_display_name`

## EspacioPublicitario (`upoferia.espacio_publicitario`) — `espacio_publicitario.py`

### `sCodigoLugar` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`

### `fAltoM` y `fAnchoM` (Float)
- Obligatorios, mayores que 0 y como mucho 30 metros — `required` / `@api.constrains`
- En el formulario, si se pasan de 30 se ajustan a 30 y se avisa al usuario — `@api.onchange`

### Relaciones
- `exhibicion_ids` (One2many → ExhibicionMarca) — exhibiciones del espacio.

### Atributos derivados
- `fSuperficieM2` (Float) — `fAltoM × fAnchoM` — `compute` + `@api.depends`

## ExhibicionMarca (`upoferia.exhibicion_marca`) — `exhibicion_marca.py`

### `sIdExhibicion` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`

### `dFechaMontaje` y `dFechaRetirada` (Date)
- No hay fecha de retirada sin fecha de montaje, y la retirada no es anterior al montaje — `@api.constrains`
- Una exhibición no se solapa con otra del mismo espacio publicitario. Sin fecha de retirada ocupa el espacio desde el montaje en adelante; sin fecha de montaje todavía no ocupa nada — `@api.constrains` con `search`

### Relaciones
- `marca_id` (Many2one → Marca) — obligatorio (`ondelete='restrict'`).
- `espacio_publicitario_id` (Many2one → EspacioPublicitario) — obligatorio (`ondelete='restrict'`).
- `tecnico_id` (Many2one → Tecnico) — opcional (`ondelete='set null'`).

### Atributos derivados
- `sEstadoExhibicion` (Selection) — se calcula con las fechas y la fecha de hoy: sin programar, programada, montada o retirada — `compute` + `@api.depends`

## Tecnico (`upoferia.tecnico`) — `tecnico.py`

### `sCodCarnetProfesional` (Char)
- Único — `_sql_constraints`

### `dFechaCaducidadCarnet` (Date)
- Si ya ha caducado, se avisa en el formulario (no impide guardar) — `@api.onchange`

### Relaciones
- `exhibicion_ids` (One2many → ExhibicionMarca) — exhibiciones que monta.

## Servicio (`upoferia.servicio`) — `servicio.py`

### `sCodigo` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`

### `sNombre` (Char)
- Obligatorio — `required`

### Relaciones
- `servicio_proveedor_ids` (One2many → ServicioProveedor) — proveedores que lo ofrecen.
- `actuacion_ids` (Many2many → Actuación de eventos) — tabla `upoferia_actuacion_servicio`, la misma que usa `servicio_ids` en Actuación.

## ServicioProveedor (`upoferia.servicio_proveedor`) — `servicio_proveedor.py`

### `fPrecioTarifa` (Float)
- Obligatorio y no menor que 0 — `required` / `@api.constrains`

### Relaciones
- `servicio_id` y `proveedor_id` (Many2one) — obligatorios (`ondelete='cascade'`).
- La pareja servicio + proveedor no se repite — `_sql_constraints`

---

# Notas sobre la documentación

Los diagramas mantienen los nombres originales de los atributos (`nombre`, `codigo_lugar`…). En el código llevan la notación húngara (`sNombre`, `sCodigoLugar`…).

Nota: los atributos `Decimal` del UML se guardan como `Float`, y `logotipo` (`Binary` en el UML) es `fields.Image`, un `Binary` de Odoo especializado en imágenes.

Nota: los campos de relación siguen la convención de Odoo (`_id` / `_ids`), porque Odoo enlaza por su `id` interno.

Nota: `tipo_aportacion` de Patrocinio no tiene valores en el E-R; se han puesto Económica y En especie.

---

# Pendiente de revisar

- **Herencia de Persona.** Según el UML, Tecnico es subtipo de Persona (`_inherits`). Hasta entonces no tiene nombre y en los desplegables aparece como «upoferia.tecnico,1».
- **`estado` de EXHIBICION_MARCA en los diagramas.** En el código es `sEstadoExhibicion`; falta añadir `/estado` en el E-R y en el UML.
