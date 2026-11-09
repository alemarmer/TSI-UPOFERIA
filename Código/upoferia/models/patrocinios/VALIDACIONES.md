# Validaciones — Patrocinios y servicios

## Marca (`upoferia.marca`) — `marca.py`

### `sNombre` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`
- Entre 2 y 50 caracteres sin contar los espacios del principio y del final — `@api.constrains`

### Relaciones
- `proveedor_id` (Many2one → Proveedor) — opcional, relación «comercializa». Si se borra el proveedor, la marca se queda sin él.
- `exhibicion_ids` (One2many → ExhibicionMarca) — exhibiciones de la marca.
- `patrocinio_ids` (One2many → Patrocinio) — eventos que patrocina.
- `producto_ids` (One2many → Producto de tesorería) — inverso de `marca_id` en Producto.
- Botón «Eliminar patrocinios» (`btn_eliminarPatrocinios`): borra los patrocinios de la marca con la tupla `(2, id)`. Hace falta para poder borrar la marca.

## Patrocinio (`upoferia.patrocinio`) — `patrocinio.py`

### `fImporteAportacion` (Float)
- No menor que 0 — `@api.constrains`

### Relaciones
- `marca_id` (Many2one → Marca) y `evento_id` (Many2one → Evento de eventos) — obligatorios. No se puede borrar una marca ni un evento que tengan patrocinios: antes hay que borrar esos patrocinios (en la marca, con el botón «Eliminar patrocinios»).
- La pareja marca + evento no se repite (clave doble del relacional) — `_sql_constraints`

### Nombre que se muestra
- Aparece como `Cruzcampo → Concierto inaugural` — `_compute_display_name`

## EspacioPublicitario (`upoferia.espacio_publicitario`) — `espacio_publicitario.py`

### `sCodigoLugar` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`

### `fAltoM` y `fAnchoM` (Float)
- Obligatorios, mayores que 0 y como mucho 30 metros — `required` / `@api.constrains`
- En el formulario, si se pasan de 30 se ajustan a 30, y si son 0 o menos se ajustan a 1, avisando al usuario — `@api.onchange` (uno para cada campo). Si no se tocan, el onchange no actúa y la regla anterior da error al guardar.

### Relaciones
- `exhibicion_ids` (One2many → ExhibicionMarca) — exhibiciones del espacio.
- `zona_caseta_id` (Many2one → ZonaCaseta) — opcional, la zona de la caseta donde está el espacio (en el relacional son dos columnas, `nombre_caseta` y `nombre_zona_caseta`, porque la clave de ZONA_CASETA es compuesta; en Odoo es un solo Many2one).

### Atributos derivados
- `fSuperficieM2` (Float) — `fAltoM × fAnchoM` — `compute` + `@api.depends`

## ExhibicionMarca (`upoferia.exhibicion_marca`) — `exhibicion_marca.py`

### `sIdExhibicion` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`
- En mayúsculas y sin espacios (por ejemplo EXH-01) — `@api.constrains`

### `dFechaMontaje` y `dFechaRetirada` (Date)
- No hay fecha de retirada sin fecha de montaje, y la retirada no es anterior al montaje — `@api.constrains`
- Una exhibición no se solapa con otra del mismo espacio publicitario. Sin fecha de retirada ocupa el espacio desde el montaje en adelante; sin fecha de montaje todavía no ocupa nada — `@api.constrains` con `search`

### Relaciones
- `marca_id` (Many2one → Marca) — obligatorio. No se puede borrar una marca que tenga exhibiciones.
- `espacio_publicitario_id` (Many2one → EspacioPublicitario) — obligatorio. No se puede borrar un espacio que tenga exhibiciones.
- `tecnico_id` (Many2one → Tecnico) — opcional. Si se borra el técnico, la exhibición se queda sin él.

### Atributos derivados
- `sEstadoExhibicion` (Selection) — se calcula con las fechas y la fecha de hoy: sin programar, programada, montada o retirada — `compute` + `@api.depends`

## Tecnico (`upoferia.tecnico`) — `tecnico.py`

### Herencia
- Tecnico es subtipo de Persona (en el relacional su clave `dni` es clave ajena de PERSONA): hereda sus campos con `_inherits = {'upoferia.persona': 'persona_id'}`, como en el ejemplo del Tema 5.
- En los desplegables aparece con el nombre de su persona (`_rec_name = 'sNombre'`, el campo heredado de Persona).
- `persona_id` (Many2one → Persona) — obligatorio, con `ondelete='cascade'`, que Odoo exige para `_inherits`.

### `sCodCarnetProfesional` (Char)
- Único — `_sql_constraints`

### `dFechaCaducidadCarnet` (Date)
- Si ya ha caducado, se avisa en el formulario (no impide guardar) — `@api.onchange`

### Relaciones
- `exhibicion_ids` (One2many → ExhibicionMarca) — exhibiciones que monta.
- `mantenimiento_ids` (Many2many → Mantenimiento) — tabla `upoferia_mantenimiento_tecnico` (MANTENIMIENTO_TECNICO en el relacional), la misma que debe usar Mantenimiento.
- Botón «Quitar exhibiciones» (`btn_quitarExhibiciones`): deja sus exhibiciones sin técnico con la tupla `(5,)`; las exhibiciones no se borran.

## Servicio (`upoferia.servicio`) — `servicio.py`

### `sCodigo` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`

### `sNombre` (Char)
- Obligatorio — `required`
- Entre 2 y 50 caracteres sin contar los espacios del principio y del final — `@api.constrains`

### Relaciones
- `servicio_proveedor_ids` (One2many → ServicioProveedor) — proveedores que lo ofrecen.
- `incidencia_ids` (One2many → Incidencia) — inverso de `servicio_id` en Incidencia.
- `actuacion_ids` (Many2many → Actuación de eventos) — tabla `upoferia_actuacion_servicio`, la misma que usa `servicio_ids` en Actuación.
- Botón «Eliminar tarifas» (`btn_eliminarTarifas`): borra las tarifas del servicio con la tupla `(2, id)`. Hace falta para poder borrar el servicio.

## ServicioProveedor (`upoferia.servicio_proveedor`) — `servicio_proveedor.py`

### `fPrecioTarifa` (Float)
- Obligatorio y no menor que 0 — `required` / `@api.constrains`

### Relaciones
- `servicio_id` y `proveedor_id` (Many2one) — obligatorios. No se puede borrar un servicio ni un proveedor que tengan tarifas: antes hay que borrarlas con el botón «Eliminar tarifas».
- La pareja servicio + proveedor no se repite — `_sql_constraints`

---

# Notas sobre la documentación

Los diagramas mantienen los nombres originales de los atributos (`nombre`, `codigo_lugar`…). En el código llevan la notación húngara (`sNombre`, `sCodigoLugar`…).

Nota: los atributos `Decimal` del UML se guardan como `Float`, y `logotipo` (`Binary` en el UML) es `fields.Image`, un `Binary` de Odoo especializado en imágenes.

Nota: los campos de relación siguen la convención de Odoo (`_id` / `_ids`), porque Odoo enlaza por su `id` interno.

Nota: `tipo_aportacion` de Patrocinio no tiene valores en el E-R; se han puesto Económica y En especie.

Nota: las relaciones no llevan `ondelete` (salvo `persona_id` de Tecnico, que lo exige `_inherits`), así que Odoo aplica su comportamiento por defecto: si el Many2one es obligatorio no deja borrar el registro al que apunta, y si es opcional lo borra y deja el campo vacío. Para poder borrar un registro que tiene otros que dependen de él, se usan los botones `btn_eliminar...`, que borran antes esos registros con `write` y la tupla `(2, id)`, como se vio en el Tema 6_2.

---

# Pendiente de revisar

- **`estado` de EXHIBICION_MARCA en los diagramas.** En el código es `sEstadoExhibicion`; falta añadir `/estado` en el E-R y en el UML.
- **Nombres que deben usar los compañeros.** Se supone que existen `upoferia.persona` (con su nombre en el campo `sNombre`), `upoferia.zona_caseta`, `upoferia.evento`, `upoferia.producto` (con un Many2one `marca_id`), `upoferia.actuacion` (con la tabla `upoferia_actuacion_servicio`), `upoferia.incidencia` (con un Many2one `servicio_id`) y `upoferia.mantenimiento` (con la tabla `upoferia_mantenimiento_tecnico`). Hasta que estén en la rama, el módulo no se instala.