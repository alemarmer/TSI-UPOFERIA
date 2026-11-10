## Caseta (`upoferia.caseta`) — `caseta.py`

### `sNombre` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`
- No vacío ni solo espacios — `@api.constrains`
- Sin espacios al principio ni al final — `@api.constrains`
- Entre 2 y 100 caracteres — `@api.constrains`

### `sCalle` (Char)
- Si se indica: no solo espacios, sin espacios al principio ni al final — `@api.constrains`
- Entre 2 y 100 caracteres — `@api.constrains`

### `sNumero` (Char)
- Exige que haya calle — `@api.constrains`
- Como mucho 10 caracteres — `@api.constrains`
- Un número con letra mayúscula opcional, o un rango con guion, sin espacios (ej. `12`, `12B`, `45-47`) — `@api.constrains`
- La pareja calle + número no se repite (dos casetas no pueden estar en la misma dirección) — `_sql_constraints` `UNIQUE ("sCalle", "sNumero")`

### `iModulos` (Integer)
- Obligatorio (por defecto 1) — `required`
- Entre 1 y 20 — `@api.constrains`

### `iAforoAutorizado` (Integer)
- Obligatorio — `required`
- Entre 1 y 5.000 personas — `@api.constrains`

### `fHoraApertura` (Float)
- Entre las 00:00 y las 23:59 (`0 <= hora < 24`) — `@api.constrains`

### `fHoraCierre` (Float)
- Entre las 00:00 y las 23:59 (`0 <= hora < 24`) — `@api.constrains`
- No se exige que sea posterior a la apertura, porque las casetas cierran de madrugada.

### Relaciones
- `zona_ids` (One2many → ZonaCaseta) — zonas de la caseta (inverso de `caseta_id`).
- `mobiliario_ids` (One2many → MobiliarioCaseta) — mobiliario asignado a la caseta (inverso de `caseta_id`).
- `licencia_ids` (One2many → Licencia) — licencias de la caseta (inverso de `caseta_id`).
- `inspeccion_ids` (One2many → Inspeccion) — inspecciones de la caseta (inverso de `caseta_id`, bloque Inspecciones e Incidencias).

## ZonaCaseta (`upoferia.zona_caseta`) — `zona_caseta.py`

### `sNombre` (Char) — clave (junto con la caseta)
- Obligatorio — `required`
- No vacío ni solo espacios — `@api.constrains`
- Sin espacios al principio ni al final — `@api.constrains`
- Entre 2 y 50 caracteres — `@api.constrains`

### `sTipo` (Selection)
- Lista cerrada: comedor, barra, cocina, baile, escenario, reservado, almacen, aseos — `fields.Selection`

### `fSuperficieM2` (Float)
- No menor que 0 — `@api.constrains`
- Como mucho 5.000 m² — `@api.constrains`
- Como mucho dos decimales — `@api.constrains`

### Relaciones
- `caseta_id` (Many2one → Caseta) — obligatorio (`required`), entidad débil: si se borra la caseta se borran sus zonas - unlink de Caseta.
- La pareja caseta + `sNombre` no se repite (clave de la entidad débil) — `_sql_constraints` `UNIQUE (caseta_id, "sNombre")`.
- `mesa_ids` (One2many → Mesa) — mesas de la zona (inverso de `zona_id`).

### Nombre que se muestra
- En los desplegables una zona aparece con su caseta (ej. `El Rebujito / Comedor`) — `_compute_display_name` con `@api.depends`
- Se puede buscar por el nombre de la zona o por el de la caseta — `_rec_names_search`

## Mesa (`upoferia.mesa`) — `mesa.py`

### `iNumero` (Integer) — clave
- Obligatorio y único — `required` / `_sql_constraints`
- Entre 1 y 9999 — `@api.constrains`

### `iCapacidad` (Integer)
- Obligatorio — `required`
- Entre 1 y 50 personas — `@api.constrains`

### Relaciones
- `zona_id` (Many2one → ZonaCaseta) — opcional; si se borra la zona, la mesa se queda sin zona (comportamiento por defecto de Odoo en un Many2one opcional). La FK compuesta `nombre_caseta, nombre_zona_caseta` del relacional se convierte en este único Many2one.

### Nombre que se muestra
- `Mesa 12 (El Rebujito / Comedor)`, o `Mesa 12` si no tiene zona — `_compute_display_name` con `@api.depends`

## MobiliarioCaseta (`upoferia.mobiliario_caseta`) — `mobiliario_caseta.py`

### `sNumeroSerie` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`
- No vacío ni solo espacios — `@api.constrains`
- Entre 2 y 30 caracteres — `@api.constrains`
- Código en mayúsculas, sin espacios (ej. `EXT-2026-0001`) — `@api.constrains`

### `sNombre` (Char)
- Obligatorio — `required`
- No vacío ni solo espacios — `@api.constrains`
- Sin espacios al principio ni al final — `@api.constrains`
- Entre 2 y 100 caracteres — `@api.constrains`

### `dFechaAsignacion` (Date)
- Entre el 01/01/1970 y hoy — `@api.constrains`
- Obligatoria si el mobiliario tiene caseta, y prohibida si no la tiene — `@api.constrains`

### `fCoste` (Float)
- No menor que 0 — `@api.constrains`
- Como mucho 1.000.000 € — `@api.constrains`
- Como mucho dos decimales (céntimos) — `@api.constrains`

### Relaciones
- `caseta_id` (Many2one → Caseta) — opcional; si se borra la caseta, el mobiliario se queda sin caseta y sin fecha de asignación — unlink de Caseta. **No está en el relacional** (ver notas).

## ElementoSeguridad (`upoferia.elemento_seguridad`) — `elemento_seguridad.py`

### Herencia
- Subtipo de MobiliarioCaseta con herencia por delegación (`_inherits`). Cada elemento de seguridad tiene su registro de mobiliario, así que también tiene `sNumeroSerie`, `sNombre`, `dFechaAsignacion`, `fCoste` y `caseta_id`, con las mismas validaciones.
- `mobiliario_id` (Many2one → MobiliarioCaseta) — obligatorio (`required`); si se borra el mobiliario se borra el elemento de seguridad - Al borrar un elemento de seguridad se borra también su mobiliario, porque el elemento es ese mobiliario — unlink.
- Un mobiliario solo puede ser un elemento de seguridad — `_sql_constraints` `UNIQUE (mobiliario_id)`

### `sTipo` (Selection)
- Obligatorio — `required`
- Lista cerrada: extintor, botiquin, detector_humo, luz_emergencia, senal_evacuacion, manta_ignifuga, desfibrilador — `fields.Selection`

### `dFechaUltimaRevision` (Date)
- Entre el 01/01/1970 y hoy — `@api.constrains`

### `dFechaProximaRevision` (Date)
- Posterior a la última revisión — `@api.constrains`
- Como mucho cinco años después de la última revisión — `@api.constrains`

### Atributos derivados
- `bRevisionVencida` (Boolean) — verdadero si la próxima revisión es anterior a hoy; solo lectura, no se guarda porque depende de la fecha de hoy — `compute` + `@api.depends`

## Licencia (`upoferia.licencia`) — `licencia.py`

### `sNumeroExpediente` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`
- No vacío ni solo espacios — `@api.constrains`
- Entre 2 y 20 caracteres — `@api.constrains`
- Código en mayúsculas, sin espacios (ej. `EXP-2026/0001`) — `@api.constrains`

### `sTipo` (Selection)
- Obligatorio — `required`
- Lista cerrada: apertura, actividad, montaje, musica, sanitaria, carruaje — `fields.Selection`

### `sOrganismo` (Char)
- Si se indica: no solo espacios, sin espacios al principio ni al final — `@api.constrains`
- Entre 2 y 100 caracteres — `@api.constrains`

### `dFechaConcesion` (Date)
- Entre el 01/01/1970 y hoy — `@api.constrains`

### `dFechaCaducidad` (Date)
- Exige que haya fecha de concesión — `@api.constrains`
- No anterior a la fecha de concesión — `@api.constrains`
- Como mucho diez años después de la fecha de concesión — `@api.constrains`

### `sEstado` (Selection)
- Obligatorio (por defecto `solicitada`) — `required`
- Lista cerrada: solicitada, concedida, denegada, revocada — `fields.Selection`
- Concedida y revocada exigen las dos fechas; solicitada y denegada no pueden tener ninguna — `@api.constrains`

### `sDocumento` (Char)
- Sin espacios, como mucho 255 caracteres — `@api.constrains`
- URL `http(s)://` o archivo `.pdf/.doc/.docx/.odt` — `@api.constrains`

### Relaciones
- `caseta_id` (Many2one → Caseta) — obligatorio (`required`); no se puede borrar una caseta que tenga licencias — unlink de Caseta conUserError.

### Atributos derivados
- `bVigente` (Boolean) — verdadero si el estado es concedida y hoy está entre la fecha de concesión y la de caducidad; solo lectura, no se guarda porque depende de la fecha de hoy — `compute` + `@api.depends`

## Llave (`upoferia.llave`) — `llave.py`

### `sCodigoLlave` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`
- No vacío ni solo espacios — `@api.constrains`
- Entre 2 y 20 caracteres — `@api.constrains`
- Código en mayúsculas, sin espacios (ej. `LL-T-014`) — `@api.constrains`

### `sDescripcion` (Char)
- Sin espacios al principio ni al final — `@api.constrains`
- Como mucho 255 caracteres — `@api.constrains`

### `sTipo` (Selection)
- Obligatorio (por defecto `original`) — `required`
- Lista cerrada (dada por el E-R): maestra, original — `fields.Selection`
- Solo puede haber una llave maestra — `@api.constrains` con `search_count`

## CopiaLlave (`upoferia.copia_llave`) — `copia_llave.py`

### `iNumeroCopia` (Integer) — clave (junto con la asignación de taquilla)
- Obligatorio — `required`
- Entre 1 y 99 — `@api.constrains`

### `dFechaEntrega` (Date)
- Entre el 01/01/1970 y hoy — `@api.constrains`

### `dFechaBaja` (Date)
- Exige que haya fecha de entrega — `@api.constrains`
- No anterior a la fecha de entrega — `@api.constrains`
- No posterior a hoy — `@api.constrains`

### `sEstado` (Selection)
- Obligatorio (por defecto `activa`) — `required`
- Lista cerrada: activa, devuelta, perdida — `fields.Selection`
- Una copia activa no puede tener fecha de baja; una devuelta o perdida tiene que tenerla — `@api.constrains`

### Nombre que se muestra
- `Copia 2` — `_compute_display_name` con `@api.depends`

---

# Pendiente (relaciones con tablas de otros bloques)

- **Licencia**: `carruaje_id` (Many2one → Carruaje), opcional. Cuando esté, una licencia de tipo `carruaje` tendrá que tenerlo obligatoriamente.
- **Llave**: `taquilla_id` (Many2one → Taquilla), opcional y único (`UNIQUE (taquilla_id)`). Cuando esté: la maestra no puede tener taquilla y una llave original tiene que tenerla.
- **CopiaLlave**: `asignacion_id` (Many2one → AsignacionTaquilla), obligatorio; al borrar la asignación se borrarán sus copias (unlink). Cuando esté: `UNIQUE (asignacion_id, "iNumeroCopia")`, solo una copia activa por asignación, y el nombre que se muestra pasará a ser `Taquilla X – copia N`.
- **Caseta**: los One2many inversos de las tablas de otros bloques (eventos, transacciones…), cuando existan esos modelos.

---

# Notas sobre la documentación

Los diagramas (E-R, relacional y UML) mantienen los nombres originales de los atributos (`nombre`, `aforo_autorizado`…). En el código llevan la notación húngara (`sNombre`, `iAforoAutorizado`…), pero de momento los diagramas no se cambian.

Nota: los atributos `Time` del UML (`hora_apertura`, `hora_cierre`) se guardan como `Float` en Odoo, porque no tiene campo de hora. En la vista se usará `widget="float_time"`.

Nota: los atributos `tipo` y `estado` son `String` en el UML y `Selection` en el código, porque el E-R dice que son listas cerradas. Los valores de las listas se han decidido al programar y se pueden cambiar si el grupo acuerda otros.

Nota: en el código los campos de relación siguen la convención de Odoo que usa el profesor (`_id` / `_ids`), mientras que el relacional usa los nombres de las claves ajenas (`nombre_caseta`, `numero_taquilla`…). Las claves ajenas compuestas del relacional se convierten en un único Many2one, porque Odoo enlaza por su `id` interno.

Nota: **MOBILIARIO_CASETA no tiene clave ajena hacia CASETA en el relacional**, pero las validaciones de PUNTO_CONTROL, INCIDENCIA y MANTENIMIENTO necesitan saber de qué caseta es cada mobiliario. Se ha añadido `caseta_id` en el código; hay que añadir `nombre_caseta` (NULL) a MOBILIARIO_CASETA en el relacional.

Nota: ELEMENTO_SEGURIDAD es subtipo de MOBILIARIO_CASETA y se implementa con `_inherits`, que es lo que corresponde a «su clave es la del supertipo».

Nota: el relacional no dice qué atributos que no son clave ajena son obligatorios. Se han hecho obligatorios los que necesitan las validaciones o sin los que el registro no tiene sentido (`iModulos`, `iAforoAutorizado`, `iCapacidad`, `sNombre` del mobiliario, `sTipo` de licencia, llave y elemento de seguridad, y los `sEstado`).
