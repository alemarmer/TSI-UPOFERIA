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

---

# Notas sobre la documentación

Los diagramas (E-R, relacional y UML) mantienen los nombres originales de los atributos (`id_transaccion`, `importe`…). En el código llevan la notación húngara (`sIdTransaccion`, `fImporte`…), pero de momento los diagramas no se cambian.

Nota: los atributos `Decimal` del UML (`importe`, `precio_unitario`) se guardan como `Float` en Odoo. No hace falta cambiar el diagrama.

Nota: `estado` es `String` en el UML y `Selection` en el código, porque el E-R dice que es una lista cerrada.
