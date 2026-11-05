## TipoTransaccion (`feria.tipo_transaccion`) — `tipo_transaccion.py`

### `sCodigo` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`
- Solo admite PED, ALB, FAC, ABO o CON — `@api.constrains`

### `sNombre` (Char)
- Obligatorio — `required`
- No vacío ni solo espacios — `@api.constrains`
- Sin espacios al principio ni al final — `@api.constrains`
- Entre 2 y 50 caracteres — `@api.constrains`

### `sDescripcion` (Char)
- Sin espacios al principio ni al final — `@api.constrains`
- Como mucho 255 caracteres — `@api.constrains`

### Relaciones
- `transaccion_ids` (One2many → Transaccion) — las transacciones de este tipo (inverso de `tipo_transaccion_id`).

## Transaccion (`feria.transaccion`) — `transaccion.py`

### `sIdTransaccion` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`
- No vacío ni solo espacios — `@api.constrains`
- Entre 2 y 20 caracteres — `@api.constrains`
- Código en mayúsculas, sin espacios (ej. `PED-2026-001`) — `@api.constrains`

### `fImporte` (Float)
- No menor que 0 — `@api.constrains`
- Como mucho 10.000.000 € — `@api.constrains`
- Como mucho dos decimales (céntimos) — `@api.constrains`

### `sEstado` (Selection)
- Lista cerrada: borrador, confirmado, recibido, cancelado, previsto, hecho, pendiente, pagada, vencida, vigente, vencido, rescindido — `fields.Selection`

### `dFechaInicial` (Date)
- Entre el 01/01/1970 y dos años después de hoy — `@api.constrains`

### `dVencimiento` (Date)
- No anterior a la fecha inicial — `@api.constrains` + aviso `onchange`
- Exige que haya fecha inicial — `@api.constrains`
- Como mucho un año después de la fecha inicial — `@api.constrains`

### `dFechaPrevistaFin` (Date)
- No anterior a la fecha inicial — `@api.constrains` + aviso `onchange`
- Exige que haya fecha inicial — `@api.constrains`
- Como mucho diez años después de la fecha inicial — `@api.constrains`

### `bRenovacionAuto` (Boolean)
- Sin validaciones.

### `sDocumento` (Char)
- Sin espacios, como mucho 255 caracteres — `@api.constrains`
- URL `http(s)://` o archivo `.pdf/.doc/.docx/.odt` — `@api.constrains`

### `sRefProveedor` (Char)
- Sin espacios sobrantes, como mucho 30 caracteres — `@api.constrains`
- Solo letras, números, espacios y `- / . _` (ej. `F-2026/0001`) — `@api.constrains`

### Relaciones
- `tipo_transaccion_id` (Many2one → TipoTransaccion) — obligatorio (`required`); no se puede borrar un tipo que tenga transacciones (`ondelete='restrict'`).
- `proveedor_id` (Many2one → Proveedor) — obligatorio (`required`), relación «interviene en»; no se puede borrar un proveedor que tenga transacciones (`ondelete='restrict'`).
- `transaccion_origen_id` (Many2one → Transaccion) — opcional, relación reflexiva «genera»; si se borra la de origen, la generada se queda sin origen (`ondelete='set null'`).
- `transaccion_derivada_ids` (One2many → Transaccion) — transacciones generadas a partir de esta (inverso de `transaccion_origen_id`).
- `linea_ids` (One2many → LineaTransaccion) — líneas de la transacción (inverso de `transaccion_id`); opcional.

## LineaTransaccion (`feria.linea_transaccion`) — `linea_transaccion.py`

### `iNumeroLinea` (Integer) — clave (junto con la transacción)
- Obligatorio — `required`
- Entre 1 y 9999 — `@api.constrains`

### `iCantidad` (Integer)
- Obligatorio — `required`
- Mayor que 0 y como mucho 1.000.000 — `@api.constrains`

### `iCantidadRecibida` (Integer)
- No menor que 0 — `@api.constrains`
- No puede superar la cantidad — `@api.constrains` + aviso `onchange`

### `fPrecioUnitario` (Float)
- No menor que 0 y como mucho 1.000.000 € — `@api.constrains`

### Relaciones
- `transaccion_id` (Many2one → Transaccion) — obligatorio (`required`), entidad débil: si se borra la transacción se borran sus líneas (`ondelete='cascade'`).
- La pareja transacción + `iNumeroLinea` no se repite (clave de la entidad débil) — `_sql_constraints` `UNIQUE ("transaccion_id", "iNumeroLinea")`.
- `linea_pedido_id` (Many2one → LineaTransaccion) — opcional, relación reflexiva «se factura en»; `ondelete='set null'`.
- `linea_factura_ids` (One2many → LineaTransaccion) — líneas de factura que facturan esta línea de pedido (inverso de `linea_pedido_id`).

### Nombre que se muestra
- En los desplegables una línea aparece con el identificador de su transacción y su número (ej. `PED-2026-001 / 1`) — `_compute_display_name` con `@api.depends`
- Se puede buscar por la transacción o por el número de línea — `_rec_names_search`

---

# Notas sobre la documentación

Los diagramas (E-R, relacional y UML) mantienen los nombres originales de los atributos (`id_transaccion`, `importe`…). En el código llevan la notación húngara (`sIdTransaccion`, `fImporte`…), pero de momento los diagramas no se cambian.

Nota: los atributos `Decimal` del UML (`importe`, `precio_unitario`) se guardan como `Float` en Odoo. No hace falta cambiar el diagrama.

Nota: `estado` es `String` en el UML y `Selection` en el código, porque el E-R dice que es una lista cerrada.

Nota: en el código los campos de relación siguen la convención de Odoo que usa el profesor (`_id` / `_ids`), mientras que el relacional usa los nombres de las claves ajenas (`dni_proveedor`, `codigo_tipo_transaccion`…). Las claves ajenas compuestas del relacional se convierten en un único Many2one, porque Odoo enlaza por su `id` interno. Igual que con la notación húngara, los diagramas no se cambian.

---

# Pendiente de revisar

- **Los modelos todavía no se cargan en Odoo.** `models/__init__.py` no importa esta carpeta (ni ninguna de las otras) y `security/ir.model.access.csv` no tiene permisos para estos modelos. Hasta que se añadan, nada de esto se puede probar en Odoo.
- **Tipos de transacción.** Como `tipo_transaccion_id` es obligatorio, antes de crear transacciones tienen que existir los tipos PED, ALB, FAC, ABO y CON. Habría que cargarlos con un archivo de datos XML al instalar el módulo.
- **Validaciones con claves ajenas (pendientes):** líneas solo en PED/FAC/ABO y como mínimo una; `cantidad_recibida` solo en líneas de PED; atributos y estados permitidos según el tipo; parejas válidas de «genera» (CON → PED, CON → FAC/ABO, PED → ALB) con el mismo proveedor; PROVEEDOR + `ref_proveedor` no se repite en FAC/ABO; «se factura en» une una línea de PED con una de FAC/ABO del mismo producto.
- **Botones de cambio de estado (pendientes)** según el recorrido de estados de cada tipo, con `write`.
- **Campos calculados (pendientes):** `importe_facturado`, `subtotal`, `cantidad_facturada`.
- **Relaciones con modelos de los compañeros (pendientes):** Transaccion → Caseta (`caseta_id`) y → LineaPresupuesto (`linea_presupuesto_id`); LineaTransaccion → Producto (`producto_id`). Y al revés, Movimiento, Mantenimiento, Prestamo, Actuacion y Salida apuntan a Transaccion.
