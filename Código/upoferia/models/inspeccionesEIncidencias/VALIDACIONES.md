## Inspeccion (`upoferia.inspeccion`) — `inspeccion.py`

### `sReferencia` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`

### `sTipo` (Selection)
- Obligatorio — `required`
- Lista cerrada: seguridad, electrica, estructural, sanitaria, aforo, veterinaria — `fields.Selection`

### `dFecha` (Date)
- Obligatorio — `required`

### `sResultado` (Selection)
- Lista cerrada: favorable, favorable_condiciones, desfavorable — `fields.Selection`
- Obligatorio si la inspección está realizada — `@api.constrains`

### `sEstado` (Selection)
- Obligatorio (por defecto `programada`) — `required`
- Lista cerrada: programada, realizada, cancelada — `fields.Selection`

### Relaciones
- `caseta_id` (Many2one → Caseta) — obligatorio (`required`); no se puede borrar una caseta que tenga inspecciones — `unlink` de Caseta con `UserError`
- `caballo_id` (Many2one → Caballo) — opcional; si se borra el caballo, la inspección se queda sin él (comportamiento por defecto de Odoo en un Many2one opcional).
- `punto_control_ids` (One2many → PuntoControl) — puntos de control de la inspección (inverso de `inspeccion_id`).
- `inspeccion_inspector_ids` (One2many → InspeccionInspector) — inspectores que participan y su rol (inverso de `inspeccion_id`).

### Borrado
- Al borrar la inspección se borran sus puntos de control y sus asignaciones de inspectores — `unlink`

### Atributos derivados
- `fPorcentajeSuperado` (Float) — puntos de control con resultado `superado` / total de puntos × 100, con dos decimales; 0 si no tiene puntos. Solo lectura; se guarda (`store=True`) porque solo depende de los puntos de control — `compute` + `@api.depends`

## PuntoControl (`upoferia.punto_control`) — `punto_control.py`

### `iNumeroPunto` (Integer) — clave (junto con la inspección)
- Obligatorio — `required`

### `sDescripcion` (Char)
- Obligatorio — `required`

### `sResultado` (Selection)
- Lista cerrada: superado, no_superado, no_aplica — `fields.Selection`

### Relaciones
- `inspeccion_id` (Many2one → Inspeccion) — obligatorio (`required`), entidad débil: si se borra la inspección se borran sus puntos — `unlink` de Inspeccion
- La pareja inspección + `iNumeroPunto` no se repite (clave de la entidad débil) — `_sql_constraints` `UNIQUE (inspeccion_id, "iNumeroPunto")`
- `elemento_seguridad_id` (Many2one → ElementoSeguridad) — opcional; si se borra el elemento, el punto se queda sin él (comportamiento por defecto de Odoo en un Many2one opcional). Solo puede revisar elementos de seguridad de la caseta inspeccionada (regla del E-R) — `@api.constrains`
- `incidencia_ids` (One2many → Incidencia) — incidencias que ha detectado este punto (inverso de `punto_control_id`).

### Nombre que se muestra
- La referencia de su inspección y su número (ej. `INS-2026-001 / 3`) — `_compute_display_name` con `@api.depends`
- Se puede buscar por la inspección o por el número de punto — `_rec_names_search`

## Incidencia (`upoferia.incidencia`) — `incidencia.py`

### `sReferencia` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`

### `dFecha` (Date)
- Obligatorio (por defecto hoy) — `required`

### `sPrioridad` (Selection)
- Obligatorio (por defecto `media`) — `required`
- Lista cerrada: baja, media, alta, urgente — `fields.Selection`

### `sEstado` (Selection)
- Obligatorio (por defecto `abierta`) — `required`
- Lista cerrada: abierta, en_curso, resuelta, cancelada — `fields.Selection`

### Relaciones
- `mobiliario_id` (Many2one → MobiliarioCaseta) — opcional; si se borra el mobiliario, la incidencia se queda sin él (comportamiento por defecto de Odoo en un Many2one opcional).
- `servicio_id` (Many2one → Servicio) — opcional; si se borra el servicio, la incidencia se queda sin él (comportamiento por defecto de Odoo en un Many2one opcional).
- `punto_control_id` (Many2one → PuntoControl) — opcional; si se borra el punto, la incidencia se queda sin él (comportamiento por defecto de Odoo en un Many2one opcional). La FK compuesta `referencia_inspeccion, numero_punto` del relacional se convierte en este único Many2one.
  - Si la detecta un punto de control, el mobiliario afectado es de la caseta inspeccionada (regla del E-R) — `@api.constrains`
- `mantenimiento_ids` (One2many → Mantenimiento) — mantenimientos que resuelven la incidencia (inverso de `incidencia_id`).

### Borrado
- No se puede borrar una incidencia que tenga mantenimientos, porque un correctivo se quedaría sin incidencia — `unlink` con `UserError`

## Mantenimiento (`upoferia.mantenimiento`) — `mantenimiento.py`

### `sIdMantenimiento` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`

### `sAsunto` (Char)
- Obligatorio — `required`

### `sTipoMantenimiento` (Selection)
- Obligatorio — `required`
- Lista cerrada: preventivo, correctivo — `fields.Selection`
- Un mantenimiento correctivo tiene que estar asociado a una incidencia — `@api.constrains`

### `dFechaSolicitud` (Date)
- Obligatorio (por defecto hoy) — `required`

### `dFechaProgramada` (Date)
- No anterior a la fecha de solicitud — `@api.constrains`

### `sEstado` (Selection)
- Obligatorio (por defecto `solicitado`) — `required`
- Lista cerrada: solicitado, programado, en_curso, finalizado, cancelado — `fields.Selection`

### Relaciones
- `incidencia_id` (Many2one → Incidencia) — opcional; no se puede borrar una incidencia que tenga mantenimientos — `unlink` de Incidencia
- `transaccion_id` (Many2one → Transaccion) — opcional, contrato que cubre el mantenimiento; si se borra la transacción, el mantenimiento se queda sin ella (comportamiento por defecto de Odoo en un Many2one opcional). Solo puede ser un contrato (transacción de tipo `CON`) — `@api.constrains`
- `tecnico_ids` (Many2many → Tecnico) — técnicos que hacen el mantenimiento. Es la tabla MANTENIMIENTO_TECNICO del relacional (`upoferia_mantenimiento_tecnico_rel`); no necesita modelo propio porque no tiene atributos.

## Inspector (`upoferia.inspector`) — `inspector.py`

### Herencia
- Subtipo de Persona con herencia por delegación (`_inherits`). Cada inspector tiene su registro de persona, así que también tiene sus campos, con las mismas validaciones.
- `persona_id` (Many2one → Persona) — obligatorio (`required`); si se borra la persona se borra el inspector (Odoo lo fuerza siempre en el campo de un `_inherits`).

### `sNumeroAcreditacion` (Char)
- Obligatorio y único — `required` / `_sql_constraints`

### Relaciones
- `inspeccion_inspector_ids` (One2many → InspeccionInspector) — inspecciones en las que participa y su rol (inverso de `inspector_id`).

### Borrado
- Al borrar el inspector se borran sus asignaciones a inspecciones — `unlink`

## InspeccionInspector (`upoferia.inspeccion_inspector`) — `inspeccion_inspector.py`

Tabla de relación N:M entre Inspeccion e Inspector. Es un modelo propio (y no un `Many2many`) porque tiene el atributo `rol`.

### Relaciones
- `inspeccion_id` (Many2one → Inspeccion) — obligatorio (`required`); si se borra la inspección se borra la asignación — `unlink` de Inspeccion
- `inspector_id` (Many2one → Inspector) — obligatorio (`required`); si se borra el inspector se borra la asignación — `unlink` de Inspector
- Un inspector no puede estar dos veces en la misma inspección (clave de la tabla) — `_sql_constraints` `UNIQUE (inspeccion_id, inspector_id)`

### Nombre que se muestra
- El del inspector — `_rec_name = 'inspector_id'`

---

# Notas sobre la documentación

Nota: los atributos `tipo`, `estado`, `prioridad` y `resultado` son `String` en el UML y `Selection` en el código, porque el E-R dice que son listas cerradas. Los valores de las listas se han decidido al programar y se pueden cambiar si el grupo acuerda otros. El valor `superado` de PuntoControl es el que usa el cálculo de `fPorcentajeSuperado`.

Nota: INSPECTOR es subtipo de PERSONA y se implementa con `_inherits`, que es lo que corresponde a «su clave (dni) es la del supertipo». Persona es un modelo del bloque Socios.
