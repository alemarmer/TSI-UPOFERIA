## Inspeccion (`feria.inspeccion`) — `inspeccion.py`

### `sReferencia` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`
- No vacío ni solo espacios — `@api.constrains`
- Entre 2 y 20 caracteres — `@api.constrains`
- Código en mayúsculas, sin espacios (ej. `INS-2026-001`) — `@api.constrains`

### `sTipo` (Selection)
- Obligatorio — `required`
- Lista cerrada: seguridad, electrica, estructural, sanitaria, aforo, veterinaria — `fields.Selection`

### `sOrganismo` (Char)
- Si se indica: no solo espacios, sin espacios al principio ni al final — `@api.constrains`
- Entre 2 y 100 caracteres — `@api.constrains`

### `dFecha` (Date)
- Obligatorio — `required`
- Entre el 01/01/1970 y un año después de hoy (se pueden programar inspecciones) — `@api.constrains`
- Si la inspección está realizada, no puede ser posterior a hoy — `@api.constrains`

### `sResultado` (Selection)
- Lista cerrada: favorable, favorable_condiciones, desfavorable — `fields.Selection`
- Obligatorio si la inspección está realizada, y prohibido si no lo está — `@api.constrains`

### `sDocumento` (Char)
- Sin espacios, como mucho 255 caracteres — `@api.constrains`
- URL `http(s)://` o archivo `.pdf/.doc/.docx/.odt` — `@api.constrains`

### `sEstado` (Selection)
- Obligatorio (por defecto `programada`) — `required`
- Lista cerrada: programada, realizada, cancelada — `fields.Selection`
- No puede dejar de estar realizada si sus puntos de control ya tienen resultado — `@api.constrains`

### Relaciones
- `caseta_id` (Many2one → Caseta) — obligatorio (`required`); no se puede borrar una caseta que tenga inspecciones (`ondelete='restrict'`).
- `punto_control_ids` (One2many → PuntoControl) — puntos de control de la inspección (inverso de `inspeccion_id`).
- `inspeccion_inspector_ids` (One2many → InspeccionInspector) — inspectores que participan y su rol (inverso de `inspeccion_id`).

### Atributos derivados
- `fPorcentajeSuperado` (Float) — puntos de control con resultado `superado` / total de puntos × 100, con dos decimales; 0 si no tiene puntos. Solo lectura; se guarda (`store=True`) porque solo depende de los puntos de control — `compute` + `@api.depends`

## PuntoControl (`feria.punto_control`) — `punto_control.py`

### `iNumeroPunto` (Integer) — clave (junto con la inspección)
- Obligatorio — `required`
- Entre 1 y 999 — `@api.constrains`

### `sDescripcion` (Char)
- Obligatorio — `required`
- No vacío ni solo espacios — `@api.constrains`
- Sin espacios al principio ni al final — `@api.constrains`
- Entre 2 y 255 caracteres — `@api.constrains`

### `sResultado` (Selection)
- Lista cerrada: superado, no_superado, no_aplica — `fields.Selection`
- Solo se puede indicar si la inspección está realizada — `@api.constrains`

### `sObservaciones` (Text)
- Sin espacios al principio ni al final — `@api.constrains`
- Como mucho 2.000 caracteres — `@api.constrains`
- Obligatorias si el punto no está superado (hay que explicar el motivo) — `@api.constrains`

### Relaciones
- `inspeccion_id` (Many2one → Inspeccion) — obligatorio (`required`), entidad débil: si se borra la inspección se borran sus puntos (`ondelete='cascade'`).
- La pareja inspección + `iNumeroPunto` no se repite (clave de la entidad débil) — `_sql_constraints` `UNIQUE (inspeccion_id, "iNumeroPunto")`.
- `elemento_seguridad_id` (Many2one → ElementoSeguridad) — opcional; si se borra el elemento, el punto se queda sin él (`ondelete='set null'`). Solo puede revisar elementos de seguridad de la caseta inspeccionada — `@api.constrains`
- `incidencia_ids` (One2many → Incidencia) — incidencias que ha detectado este punto (inverso de `punto_control_id`).

### Nombre que se muestra
- La referencia de su inspección y su número (ej. `INS-2026-001 / 3`) — `_compute_display_name` con `@api.depends`
- Se puede buscar por la inspección o por el número de punto — `_rec_names_search`

## Incidencia (`feria.incidencia`) — `incidencia.py`

### `sReferencia` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`
- No vacío ni solo espacios — `@api.constrains`
- Entre 2 y 20 caracteres — `@api.constrains`
- Código en mayúsculas, sin espacios (ej. `INC-2026-001`) — `@api.constrains`

### `dFecha` (Date)
- Obligatorio (por defecto hoy) — `required`
- Entre el 01/01/1970 y hoy — `@api.constrains`
- No anterior a la fecha de la inspección que la detecta — `@api.constrains`

### `sPrioridad` (Selection)
- Obligatorio (por defecto `media`) — `required`
- Lista cerrada: baja, media, alta, urgente — `fields.Selection`

### `sEstado` (Selection)
- Obligatorio (por defecto `abierta`) — `required`
- Lista cerrada: abierta, en_curso, resuelta, cancelada — `fields.Selection`

### Relaciones
- `mobiliario_id` (Many2one → MobiliarioCaseta) — opcional; si se borra el mobiliario, la incidencia se queda sin él (`ondelete='set null'`).
- `punto_control_id` (Many2one → PuntoControl) — opcional, `ondelete='set null'`. La FK compuesta `referencia_inspeccion, numero_punto` del relacional se convierte en este único Many2one.
  - Solo la puede detectar un punto de control no superado — `@api.constrains`
  - Si la detecta un punto de control, el mobiliario afectado es de la caseta inspeccionada — `@api.constrains`
- `mantenimiento_ids` (One2many → Mantenimiento) — mantenimientos que resuelven la incidencia (inverso de `incidencia_id`).

## Mantenimiento (`feria.mantenimiento`) — `mantenimiento.py`

### `sIdMantenimiento` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`
- No vacío ni solo espacios — `@api.constrains`
- Entre 2 y 20 caracteres — `@api.constrains`
- Código en mayúsculas, sin espacios (ej. `MNT-2026-001`) — `@api.constrains`

### `sAsunto` (Char)
- Obligatorio — `required`
- No vacío ni solo espacios — `@api.constrains`
- Sin espacios al principio ni al final — `@api.constrains`
- Entre 2 y 100 caracteres — `@api.constrains`

### `sTipoMantenimiento` (Selection)
- Obligatorio — `required`
- Lista cerrada: preventivo, correctivo — `fields.Selection`
- Un correctivo tiene que tener incidencia; un preventivo no puede tenerla — `@api.constrains`

### `dFechaSolicitud` (Date)
- Obligatorio (por defecto hoy) — `required`
- Entre el 01/01/1970 y hoy — `@api.constrains`
- No anterior a la fecha de la incidencia — `@api.constrains`

### `dFechaProgramada` (Date)
- No anterior a la fecha de solicitud — `@api.constrains`
- Como mucho un año después de la fecha de solicitud — `@api.constrains`

### `fDuracionHoras` (Float)
- No menor que 0 — `@api.constrains`
- Como mucho 500 horas — `@api.constrains`
- Como mucho dos decimales — `@api.constrains`

### `sEstado` (Selection)
- Obligatorio (por defecto `solicitado`) — `required`
- Lista cerrada: solicitado, programado, en_curso, finalizado, cancelado — `fields.Selection`
- Programado, en curso y finalizado exigen fecha programada; finalizado exige una duración mayor que 0 — `@api.constrains`
- En curso y finalizado no pueden tener la fecha programada posterior a hoy — `@api.constrains`

### Relaciones
- `incidencia_id` (Many2one → Incidencia) — opcional; si se borra la incidencia, el mantenimiento se queda sin ella (`ondelete='set null'`).

## Inspector (`feria.inspector`) — `inspector.py`

### `sNumeroAcreditacion` (Char)
- Obligatorio y único (mientras no esté la herencia de PERSONA, es lo que identifica al inspector) — `required` / `_sql_constraints`
- No vacío ni solo espacios — `@api.constrains`
- Entre 2 y 20 caracteres — `@api.constrains`
- Código en mayúsculas, sin espacios (ej. `ACR-SEV-0042`) — `@api.constrains`

### `sOrganismo` (Char)
- Si se indica: no solo espacios, sin espacios al principio ni al final — `@api.constrains`
- Entre 2 y 100 caracteres — `@api.constrains`

### `sCargo` (Char)
- Si se indica: no solo espacios, sin espacios al principio ni al final — `@api.constrains`
- Entre 2 y 100 caracteres — `@api.constrains`

### Relaciones
- `inspeccion_inspector_ids` (One2many → InspeccionInspector) — inspecciones en las que participa y su rol (inverso de `inspector_id`).

## InspeccionInspector (`feria.inspeccion_inspector`) — `inspeccion_inspector.py`

Tabla de relación N:M entre Inspeccion e Inspector. Es un modelo propio (y no un `Many2many`) porque tiene el atributo `rol`.

### `sRol` (Char)
- Si se indica: no solo espacios, sin espacios al principio ni al final — `@api.constrains`
- Entre 2 y 100 caracteres — `@api.constrains`

### Relaciones
- `inspeccion_id` (Many2one → Inspeccion) — obligatorio (`required`); si se borra la inspección se borra la asignación (`ondelete='cascade'`).
- `inspector_id` (Many2one → Inspector) — obligatorio (`required`); si se borra el inspector se borra la asignación (`ondelete='cascade'`).
- Un inspector no puede estar dos veces en la misma inspección (clave de la tabla) — `_sql_constraints` `UNIQUE (inspeccion_id, inspector_id)`.

### Nombre que se muestra
- El del inspector — `_rec_name = 'inspector_id'`

---

# Pendiente (relaciones con tablas de otros bloques)

- **Inspector**: herencia de Persona con `_inherits` (`persona_id`, obligatorio, `ondelete='cascade'`). Cuando esté, el nombre que se muestra pasará a ser el de la persona.
- **Inspeccion**: `caballo_id` (Many2one → Caballo), opcional, `ondelete='set null'`. Cuando esté, una inspección veterinaria tendrá que tener caballo.
- **Incidencia**: `servicio_id` (Many2one → `feria.servicio`), opcional, `ondelete='set null'`.
- **Mantenimiento**:
  - `transaccion_id` (Many2one → `feria.transaccion`), opcional, `ondelete='set null'` (contrato que cubre el mantenimiento).
  - `tecnico_ids` (Many2many → Tecnico): es la tabla MANTENIMIENTO_TECNICO. No necesita modelo propio porque no tiene atributos.
  - El contrato que lo cubre es de la misma caseta que el mobiliario de la incidencia — `@api.constrains`
  - Si la incidencia la origina un servicio, el contrato es con un proveedor que lo ofrece (`servicio_id.servicio_proveedor_ids`) — `@api.constrains`

---

# Notas sobre la documentación

Los diagramas (E-R, relacional y UML) mantienen los nombres originales de los atributos (`referencia`, `numero_punto`…). En el código llevan la notación húngara (`sReferencia`, `iNumeroPunto`…), pero de momento los diagramas no se cambian.

Nota: los atributos `tipo`, `estado`, `prioridad` y `resultado` son `String` en el UML y `Selection` en el código, porque el E-R dice que son listas cerradas. Los valores de las listas se han decidido al programar y se pueden cambiar si el grupo acuerda otros. El valor `superado` de PuntoControl es el que usa el cálculo de `fPorcentajeSuperado`.

Nota: en el código los campos de relación siguen la convención de Odoo que usa el profesor (`_id` / `_ids`), mientras que el relacional usa los nombres de las claves ajenas (`nombre_caseta`, `referencia_inspeccion`…). Las claves ajenas compuestas del relacional se convierten en un único Many2one, porque Odoo enlaza por su `id` interno.

Nota: las validaciones «misma caseta» de PuntoControl e Incidencia usan el `caseta_id` de MobiliarioCaseta, que se ha añadido en el código aunque no está en el relacional (ver el VALIDACIONES.md del bloque Caseta e Instalaciones).

Nota: además de las validaciones del E-R, se han añadido reglas de coherencia entre estado, fechas y resultado (por ejemplo, una inspección realizada tiene que tener resultado, o un mantenimiento correctivo tiene que tener incidencia). Se han decidido al programar.
