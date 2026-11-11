## Caseta (`upoferia.caseta`) — `caseta.py`

### `sNombre` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`

### `iModulos` (Integer)
- Obligatorio (por defecto 1) — `required`
- Mayor que 0 — `@api.constrains`

### `iAforoAutorizado` (Integer)
- Obligatorio — `required`
- Mayor que 0 — `@api.constrains`

### Relaciones
- `zona_ids` (One2many → ZonaCaseta) — zonas de la caseta (inverso de `caseta_id`).
- `mobiliario_ids` (One2many → MobiliarioCaseta) — mobiliario asignado a la caseta (inverso de `caseta_id`).
- `licencia_ids` (One2many → Licencia) — licencias de la caseta (inverso de `caseta_id`).
- `inspeccion_ids` (One2many → Inspeccion) — inspecciones de la caseta (inverso de `caseta_id`, bloque Inspecciones e Incidencias).

### Borrado
- No se puede borrar una caseta que tenga licencias o inspecciones — `unlink` con `UserError`
- Al borrar la caseta se borran sus zonas (entidad débil) — `unlink`
- Al borrar la caseta, su mobiliario se queda sin caseta y sin fecha de asignación — `unlink`

## ZonaCaseta (`upoferia.zona_caseta`) — `zona_caseta.py`

### `sNombre` (Char) — clave (junto con la caseta)
- Obligatorio — `required`

### `sTipo` (Selection)
- Lista cerrada: comedor, barra, cocina, baile, escenario, reservado, almacen, aseos — `fields.Selection`

### `fSuperficieM2` (Float)
- No menor que 0 — `@api.constrains`

### Relaciones
- `caseta_id` (Many2one → Caseta) — obligatorio (`required`), entidad débil: si se borra la caseta se borran sus zonas — `unlink` de Caseta
- La pareja caseta + `sNombre` no se repite (clave de la entidad débil) — `_sql_constraints` `UNIQUE (caseta_id, "sNombre")`
- `mesa_ids` (One2many → Mesa) — mesas de la zona (inverso de `zona_id`).

### Nombre que se muestra
- En los desplegables una zona aparece con su caseta (ej. `El Rebujito / Comedor`) — `_compute_display_name` con `@api.depends`
- Se puede buscar por el nombre de la zona o por el de la caseta — `_rec_names_search`

## Mesa (`upoferia.mesa`) — `mesa.py`

### `iNumero` (Integer) — clave
- Obligatorio y único — `required` / `_sql_constraints`

### `iCapacidad` (Integer)
- Obligatorio — `required`
- Mayor que 0 — `@api.constrains`

### Relaciones
- `zona_id` (Many2one → ZonaCaseta) — opcional; si se borra la zona, la mesa se queda sin zona (comportamiento por defecto de Odoo en un Many2one opcional). La FK compuesta `nombre_caseta, nombre_zona_caseta` del relacional se convierte en este único Many2one.

### Nombre que se muestra
- `Mesa 12 (El Rebujito / Comedor)`, o `Mesa 12` si no tiene zona — `_compute_display_name` con `@api.depends`

## MobiliarioCaseta (`upoferia.mobiliario_caseta`) — `mobiliario_caseta.py`

### `sNumeroSerie` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`

### `sNombre` (Char)
- Obligatorio — `required`

### `fCoste` (Float)
- No menor que 0 — `@api.constrains`

### Relaciones
- `caseta_id` (Many2one → Caseta) — opcional; si se borra la caseta, el mobiliario se queda sin caseta y sin fecha de asignación — `unlink` de Caseta. **No está en el relacional** (ver notas).

## ElementoSeguridad (`upoferia.elemento_seguridad`) — `elemento_seguridad.py`

### Herencia
- Subtipo de MobiliarioCaseta con herencia por delegación (`_inherits`). Cada elemento de seguridad tiene su registro de mobiliario, así que también tiene `sNumeroSerie`, `sNombre`, `dFechaAsignacion`, `fCoste` y `caseta_id`, con las mismas validaciones.
- `mobiliario_id` (Many2one → MobiliarioCaseta) — obligatorio (`required`); si se borra el mobiliario se borra el elemento de seguridad (Odoo lo fuerza siempre en el campo de un `_inherits`).
- Un mobiliario solo puede ser un elemento de seguridad — `_sql_constraints` `UNIQUE (mobiliario_id)`
- Al borrar un elemento de seguridad se borra también su mobiliario, porque el elemento es ese mobiliario — `unlink`

### `sTipo` (Selection)
- Obligatorio — `required`
- Lista cerrada: extintor, botiquin, detector_humo, luz_emergencia, senal_evacuacion, manta_ignifuga, desfibrilador — `fields.Selection`

### `dFechaProximaRevision` (Date)
- Posterior a la fecha de la última revisión — `@api.constrains`

### Atributos derivados
- `bRevisionVencida` (Boolean) — verdadero si la próxima revisión es anterior a hoy; solo lectura, no se guarda porque depende de la fecha de hoy — `compute` + `@api.depends`

## Licencia (`upoferia.licencia`) — `licencia.py`

### `sNumeroExpediente` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`

### `sTipo` (Selection)
- Obligatorio — `required`
- Lista cerrada: apertura, actividad, montaje, musica, sanitaria, carruaje — `fields.Selection`

### `dFechaCaducidad` (Date)
- No anterior a la fecha de concesión — `@api.constrains`

### `sEstado` (Selection)
- Obligatorio (por defecto `solicitada`) — `required`
- Lista cerrada: solicitada, concedida, denegada, revocada — `fields.Selection`

### Relaciones
- `caseta_id` (Many2one → Caseta) — obligatorio (`required`); no se puede borrar una caseta que tenga licencias — `unlink` de Caseta con `UserError`
- `carruaje_id` (Many2one → Carruaje) — opcional; si se borra el carruaje, la licencia se queda sin él (comportamiento por defecto de Odoo en un Many2one opcional).

### Atributos derivados
- `bVigente` (Boolean) — verdadero si el estado es concedida y hoy está entre la fecha de concesión y la de caducidad; solo lectura, no se guarda porque depende de la fecha de hoy — `compute` + `@api.depends`

## Llave (`upoferia.llave`) — `llave.py`

### `sCodigoLlave` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`

### `sTipo` (Selection)
- Obligatorio (por defecto `original`) — `required`
- Lista cerrada (dada por el E-R): maestra, original — `fields.Selection`
- Solo puede haber una llave maestra — `@api.constrains` con `search_count`

### Relaciones
- `taquilla_id` (Many2one → Taquilla) — opcional; si se borra la taquilla, la llave se queda sin ella (comportamiento por defecto de Odoo en un Many2one opcional).
- Una taquilla solo puede tener una llave — `_sql_constraints` `UNIQUE (taquilla_id)`

## CopiaLlave (`upoferia.copia_llave`) — `copia_llave.py`

### `iNumeroCopia` (Integer) — clave (junto con la asignación de taquilla)
- Obligatorio — `required`

### `dFechaBaja` (Date)
- No anterior a la fecha de entrega — `@api.constrains`

### `sEstado` (Selection)
- Obligatorio (por defecto `activa`) — `required`
- Lista cerrada: activa, devuelta, perdida — `fields.Selection`

### Relaciones
- `asignacion_id` (Many2one → AsignacionTaquilla) — obligatorio (`required`), entidad débil: no se puede borrar una asignación que tenga copias (comportamiento por defecto de Odoo en un Many2one obligatorio).
- La pareja asignación + `iNumeroCopia` no se repite (clave de la entidad débil) — `_sql_constraints` `UNIQUE (asignacion_id, "iNumeroCopia")`

### Nombre que se muestra
- `Copia 2` — `_compute_display_name` con `@api.depends`

---

# Notas sobre la documentación

Nota: los atributos `Time` del UML (`hora_apertura`, `hora_cierre`) se guardan como `Float` en Odoo, porque no tiene campo de hora. En la vista se usa `widget="float_time"`.

Nota: los atributos `tipo` y `estado` son `String` en el UML y `Selection` en el código, porque el E-R dice que son listas cerradas. Los valores de las listas se han decidido al programar y se pueden cambiar si el grupo acuerda otros.

Nota: ELEMENTO_SEGURIDAD es subtipo de MOBILIARIO_CASETA y se implementa con `_inherits`, que es lo que corresponde a «su clave es la del supertipo».
