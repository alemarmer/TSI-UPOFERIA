# Validaciones — Compras

## TipoTransaccion (`upoferia.tipo_transaccion`) — `tipo_transaccion.py`

### `sCodigo` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`
- Solo admite PED, ALB, FAC, ABO o CON — `@api.constrains`

### `sNombre` (Char)
- Obligatorio y con entre 2 y 50 caracteres sin contar los espacios del principio y del final — `required` / `@api.constrains`
### Relaciones
- `transaccion_ids` (One2many → Transaccion) — las transacciones de este tipo (inverso de `tipo_transaccion_id`).

## Transaccion (`upoferia.transaccion`) — `transaccion.py`

### `sIdTransaccion` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`

### `fImporte` (Float)
- No menor que 0 — `@api.constrains`

### `sEstado` (Selection)
- Obligatorio — `required`
- Según el tipo: PED → borrador, confirmado, recibido, cancelado; ALB → previsto, hecho; FAC y ABO → pendiente, pagada, vencida; CON → borrador, vigente, vencido, rescindido — `@api.constrains`
- Al elegir el tipo se pone el estado inicial (PED y CON → borrador, ALB → previsto, FAC y ABO → pendiente) — `@api.onchange`
- Se cambia con los botones del formulario (`btn_*`, cada uno hace un `write`, como en los ejemplos del profesor). Los botones se ven siempre; si se pulsa uno que no corresponde al tipo (por ejemplo «Confirmar» en una factura), la regla anterior da error y el estado no cambia.

### `dVencimiento` y `dFechaPrevistaFin` (Date)
- No pueden ser anteriores a la fecha inicial — `@api.constrains`

### Relaciones
- `tipo_transaccion_id` (Many2one → TipoTransaccion) — obligatorio. No se puede borrar un tipo que tenga transacciones.
- `proveedor_id` (Many2one → Proveedor) — obligatorio, relación «interviene en». No se puede borrar un proveedor que tenga transacciones.
- `transaccion_origen_id` (Many2one → Transaccion) — opcional, relación reflexiva «genera». Si se borra la de origen, la generada se queda sin origen.
- `transaccion_derivada_ids` (One2many → Transaccion) — transacciones generadas a partir de esta.
- `linea_ids` (One2many → LineaTransaccion) — líneas de la transacción.
- `linea_presupuesto_id` (Many2one → LineaPresupuesto de tesorería) — opcional. Si se borra la línea de presupuesto, la transacción se queda sin ella.
- `caseta_id` (Many2one → Caseta) — opcional, la caseta a la que se destina la transacción (`nombre_caseta` en el relacional). Si se borra la caseta, la transacción se queda sin ella.
- `movimiento_ids` (One2many → Movimiento de tesorería) — inverso de `transaccion_id` en Movimiento.
- `actuacion_ids` (One2many → Actuación de eventos) — inverso de `transaccion_id` en Actuación.
- `salida_ids` (One2many → Salida de eventos) — inverso de `transaccion_id` en Salida.
- `prestamo_ids` (One2many → Prestamo) — inverso de `transaccion_id` en Prestamo.
- `mantenimiento_ids` (One2many → Mantenimiento) — inverso de `transaccion_id` en Mantenimiento.
- Botón «Eliminar líneas» (`btn_eliminarLineas`): borra todas las líneas de la transacción con `write` y la tupla `(2, id)`. Hace falta para poder borrar una transacción, porque Odoo no deja borrar una transacción que tenga líneas.

### Atributos derivados
- `fImporteFacturado` (Float) — suma del importe de las FAC que genera esta transacción; solo lectura, no se guarda — `compute` + `@api.depends`

## LineaTransaccion (`upoferia.linea_transaccion`) — `linea_transaccion.py`

### `iNumeroLinea` (Integer) — clave (junto con la transacción)
- Obligatorio — `required`
- La pareja transacción + número de línea no se repite (clave de la entidad débil) — `_sql_constraints`

### `iCantidad` e `iCantidadRecibida` (Integer)
- La cantidad es obligatoria y mayor que 0 — `required` / `@api.constrains`
- La cantidad recibida no es menor que 0 ni mayor que la cantidad — `@api.constrains`

### `fPrecioUnitario` (Float)
- No menor que 0 — `@api.constrains`

### Relaciones
- `transaccion_id` (Many2one → Transaccion) — obligatorio, entidad débil. No se puede borrar una transacción que tenga líneas: antes hay que borrarlas con el botón «Eliminar líneas».
- `linea_pedido_id` (Many2one → LineaTransaccion) — opcional, relación reflexiva «se factura en». Si se borra la línea de pedido, la de factura se queda sin ella.
- `linea_factura_ids` (One2many → LineaTransaccion) — líneas de factura que facturan esta línea de pedido.
- `producto_id` (Many2one → Producto de tesorería) — opcional. Si se borra el producto, la línea se queda sin producto.

### Nombre que se muestra
- Aparece como `PED-2026-001 / 1` (transacción y número) — `_compute_display_name`

### Atributos derivados
- `fSubtotal` (Float) — `iCantidad × fPrecioUnitario` — `compute` + `@api.depends`
- `iCantidadFacturada` (Integer) — suma de las cantidades de sus líneas de factura — `compute` + `@api.depends`

---

# Notas sobre la documentación

Los diagramas (E-R, relacional y UML) mantienen los nombres originales de los atributos (`id_transaccion`, `importe`…). En el código llevan la notación húngara (`sIdTransaccion`, `fImporte`…).

Nota: los atributos `Decimal` del UML se guardan como `Float` en Odoo, y `estado` es `String` en el UML y `Selection` en el código, porque el E-R dice que es una lista cerrada.

Nota: los campos de relación siguen la convención de Odoo (`_id` / `_ids`). Las claves ajenas del relacional (`dni_proveedor`, `codigo_tipo_transaccion`…) se convierten en un Many2one, porque Odoo enlaza por su `id` interno.

Nota: se han dejado solo las validaciones básicas y la regla del estado según el tipo. Estas reglas del cuadro de restricciones del E-R no están programadas: atributos que solo existen en algunos tipos, parejas válidas de «genera», que las líneas solo existan en PED/FAC/ABO, que no se facture más de lo pedido, que «se factura en» una líneas del mismo producto y que la referencia del proveedor no se repita en FAC/ABO.

Nota: las relaciones no llevan `ondelete`, así que Odoo aplica su comportamiento por defecto: si el Many2one es obligatorio no deja borrar el registro al que apunta, y si es opcional lo borra y deja el campo vacío. Para poder borrar un registro que tiene otros que dependen de él, se usan los botones `btn_eliminar...`, que borran antes esos registros con `write` y la tupla `(2, id)`, como se vio en el Tema 6_2.

---

# Pendiente de revisar

- **Nombres que deben usar los compañeros.** Las relaciones inversas suponen que existen estos modelos y campos: `upoferia.movimiento`, `upoferia.actuacion`, `upoferia.salida`, `upoferia.prestamo` y `upoferia.mantenimiento` con un Many2one `transaccion_id`; `upoferia.producto`, `upoferia.linea_presupuesto` y `upoferia.caseta`. Hasta que estén en la rama, el módulo no se instala.
