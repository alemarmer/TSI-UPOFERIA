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
- Solo en PED, FAC, ABO y CON; en ALB tiene que quedar a 0 — `@api.constrains`

### `sEstado` (Selection)
- Lista cerrada: borrador, confirmado, recibido, cancelado, previsto, hecho, pendiente, pagada, vencida, vigente, vencido, rescindido — `fields.Selection`
- Según el tipo: PED → borrador, confirmado, recibido, cancelado; ALB → previsto, hecho; FAC y ABO → pendiente, pagada, vencida; CON → borrador, vigente, vencido, rescindido — `@api.constrains`
- Al elegir el tipo se pone el estado inicial (PED y CON → borrador, ALB → previsto, FAC y ABO → pendiente) — `@api.onchange`
- Solo se cambia con los botones del formulario (en la vista es de solo lectura). Recorrido permitido: PED borrador → confirmado → recibido, y borrador o confirmado → cancelado; ALB previsto → hecho; FAC y ABO pendiente → pagada, pendiente → vencida y vencida → pagada; CON borrador → vigente → vencido, y vigente → rescindido. Cualquier otro salto da error — `_cambiar_estado` con `write` + botones `action_*`
- Obligatorio (se rellena solo al elegir el tipo) — `@api.constrains`

### `dFechaInicial` (Date)
- Entre el 01/01/1970 y dos años después de hoy — `@api.constrains`

### `dVencimiento` (Date)
- No anterior a la fecha inicial — `@api.constrains` + aviso `onchange`
- Exige que haya fecha inicial — `@api.constrains`
- Como mucho un año después de la fecha inicial — `@api.constrains`
- Solo en FAC y ABO — `@api.constrains`

### `dFechaPrevistaFin` (Date)
- No anterior a la fecha inicial — `@api.constrains` + aviso `onchange`
- Exige que haya fecha inicial — `@api.constrains`
- Como mucho diez años después de la fecha inicial — `@api.constrains`

### `bRenovacionAuto` (Boolean)
- Solo en CON; en el resto tiene que estar desmarcado — `@api.constrains`
### `sDocumento` (Char)
- Sin espacios, como mucho 255 caracteres — `@api.constrains`
- URL `http(s)://` o archivo `.pdf/.doc/.docx/.odt` — `@api.constrains`
- Solo en CON — `@api.constrains`

### `sRefProveedor` (Char)
- Sin espacios sobrantes, como mucho 30 caracteres — `@api.constrains`
- Solo letras, números, espacios y `- / . _` (ej. `F-2026/0001`) — `@api.constrains`
- En FAC y ABO, un mismo proveedor no puede repetir la referencia (dos proveedores distintos sí) — `@api.constrains` con `search`

### Relaciones
- `tipo_transaccion_id` (Many2one → TipoTransaccion) — obligatorio (`required`); no se puede borrar un tipo que tenga transacciones (`ondelete='restrict'`). Solo se elige al crear la transacción; después no se puede cambiar (`readonly="id"` en la vista).
- `proveedor_id` (Many2one → Proveedor) — obligatorio (`required`), relación «interviene en»; no se puede borrar un proveedor que tenga transacciones (`ondelete='restrict'`).
- `transaccion_origen_id` (Many2one → Transaccion) — opcional, relación reflexiva «genera»; si se borra la de origen, la generada se queda sin origen (`ondelete='set null'`). Solo se admiten las parejas origen → derivada CON → PED, CON → FAC, CON → ABO y PED → ALB, y las dos tienen que ser del mismo proveedor. Se comprueba al guardar la derivada y también al cambiar el tipo o el proveedor de la de origen. Como las parejas siempre bajan de nivel, no puede haber ciclos — `@api.constrains`- `transaccion_derivada_ids` (One2many → Transaccion) — transacciones generadas a partir de esta (inverso de `transaccion_origen_id`).
- `linea_ids` (One2many → LineaTransaccion) — líneas de la transacción (inverso de `transaccion_id`). PED, FAC y ABO tienen como mínimo una línea; ALB y CON no pueden tener ninguna. Al cambiar el tipo se vuelven a comprobar las reglas de sus líneas — `@api.constrains`
### Atributos derivados
- `fImporteFacturado` (Float) — suma del importe de las transacciones FAC que genera esta (por la relación «genera»); solo lectura, no se guarda — `compute` + `@api.depends`. Solo tiene valor en CON: como solo un CON puede generar facturas, en el resto de tipos siempre es 0.
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
- Solo se puede indicar en líneas de un PED — `@api.constrains`

### `fPrecioUnitario` (Float)
- No menor que 0 y como mucho 1.000.000 € — `@api.constrains`
-Solo admite dos decimales (céntimos). — `@api.constrains`

### Relaciones
- `transaccion_id` (Many2one → Transaccion) — obligatorio (`required`), entidad débil: si se borra la transacción se borran sus líneas (`ondelete='cascade'`). Solo puede ser un PED, una FAC o un ABO — `@api.constrains`
- La pareja transacción + `iNumeroLinea` no se repite (clave de la entidad débil) — `_sql_constraints` `UNIQUE ("transaccion_id", "iNumeroLinea")`.
- `linea_pedido_id` (Many2one → LineaTransaccion) — opcional, relación reflexiva «se factura en»; `ondelete='set null'`. Solo lo pueden tener las líneas de una FAC o un ABO, y tiene que apuntar a una línea de un PED — `@api.constrains`
- `linea_factura_ids` (One2many → LineaTransaccion) — líneas de factura que facturan esta línea de pedido (inverso de `linea_pedido_id`). Solo las líneas de un PED pueden tenerlas — `@api.constrains`
- No se puede borrar la última línea de un PED, FAC o ABO (tiene que quedar como mínimo una). Sí se puede borrar la transacción entera, y con ella sus líneas — `@api.ondelete`


### Nombre que se muestra
- En los desplegables una línea aparece con el identificador de su transacción y su número (ej. `PED-2026-001 / 1`) — `_compute_display_name` con `@api.depends`
- Se puede buscar por la transacción o por el número de línea — `_rec_names_search`

### Atributos derivados
- `fSubtotal` (Float) — `iCantidad × fPrecioUnitario`; solo lectura, no se guarda — `compute` + `@api.depends`
- `iCantidadFacturada` (Integer) — suma de la cantidad de las líneas de factura que facturan esta línea de pedido (`linea_factura_ids`); solo lectura, no se guarda — `compute` + `@api.depends`
  - No puede superar la cantidad de la línea de pedido. Se comprueba al guardar la línea de factura (su cantidad o su línea de pedido) y al cambiar la cantidad de la línea de pedido — `@api.constrains` sobre `iCantidad` y `linea_pedido_id`
### Campos auxiliares
- `sCodigoTipo` (Char) — código del tipo de transacción (`related='tipo_transaccion_id.sCodigo'`); no se guarda. Solo sirve para que la vista sepa qué botones mostrar.
---

# Notas sobre la documentación

Los diagramas (E-R, relacional y UML) mantienen los nombres originales de los atributos (`id_transaccion`, `importe`…). En el código llevan la notación húngara (`sIdTransaccion`, `fImporte`…), pero de momento los diagramas no se cambian.

Nota: los atributos `Decimal` del UML (`importe`, `precio_unitario`) se guardan como `Float` en Odoo. No hace falta cambiar el diagrama.

Nota: `estado` es `String` en el UML y `Selection` en el código, porque el E-R dice que es una lista cerrada.

Nota: en el código los campos de relación siguen la convención de Odoo que usa el profesor (`_id` / `_ids`), mientras que el relacional usa los nombres de las claves ajenas (`dni_proveedor`, `codigo_tipo_transaccion`…). Las claves ajenas compuestas del relacional se convierten en un único Many2one, porque Odoo enlaza por su `id` interno. Igual que con la notación húngara, los diagramas no se cambian.

Nota: el recorrido de estados no está en los diagramas (el E-R solo dice qué estados tiene cada tipo). Se ha decidido al programar los botones.

---



