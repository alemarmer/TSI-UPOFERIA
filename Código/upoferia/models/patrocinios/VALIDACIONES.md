## Marca (`feria.marca`) — `marca.py`

### `sNombre` (Char) — clave
- Obligatorio — `required`
- Único — `_sql_constraints`
- No vacío ni solo espacios — `@api.constrains`
- Sin espacios al principio ni al final — `@api.constrains`
- Entre 2 y 100 caracteres — `@api.constrains`
- Único sin distinguir mayúsculas («Cruzcampo» = «CRUZCAMPO») — `@api.constrains`

### `binLogotipo` (Image)
- Solo admite imágenes (lo comprueba Odoo) — `fields.Image`
- Se reduce automáticamente a como mucho 512 × 512 píxeles — `max_width` / `max_height`

### `sColorCorporativo` (Char)
- Formato `#RRGGBB` o `#RGB` — `@api.constrains`

### Relaciones
- `proveedor_id` (Many2one → Proveedor) — opcional, relación «comercializa»; `ondelete='set null'`.
- `exhibicion_ids` (One2many → ExhibicionMarca) — exhibiciones de la marca (inverso de `marca_id`).

## ExhibicionMarca (`feria.exhibicion_marca`) — `exhibicion_marca.py`

### `sIdExhibicion` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`
- No vacío ni solo espacios — `@api.constrains`
- Entre 2 y 20 caracteres — `@api.constrains`
- Código en mayúsculas, sin espacios (ej. `EXH-2026-01`) — `@api.constrains`

### `dFechaMontaje` (Date)
- Entre el 01/01/1970 y dos años después de hoy — `@api.constrains`

### `dFechaRetirada` (Date)
- No anterior a la fecha de montaje — `@api.constrains` + aviso `onchange`
- Exige que haya fecha de montaje — `@api.constrains`
- Como mucho un año después del montaje — `@api.constrains`

### `sArteFinal` (Char)
- No solo espacios, sin espacios, como mucho 255 caracteres — `@api.constrains`
- URL `http(s)://` o archivo `.pdf/.png/.jpg/.jpeg/.svg/.ai/.eps/.tif/.tiff` — `@api.constrains`

### Relaciones
- `marca_id` (Many2one → Marca) — opcional, relación «aparece en»; `ondelete='set null'`.
- `tecnico_id` (Many2one → Tecnico) — opcional, relación «actualiza»; `ondelete='set null'`.
- `espacio_publicitario_id` (Many2one → EspacioPublicitario) — opcional, relación «acoge»; `ondelete='set null'`.

## EspacioPublicitario (`feria.espacio_publicitario`) — `espacio_publicitario.py`

### `sCodigoLugar` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`
- No vacío ni solo espacios — `@api.constrains`
- Entre 2 y 20 caracteres — `@api.constrains`
- Código en mayúsculas, sin espacios (ej. `PORTADA-01`) — `@api.constrains`

### `fAltoM` y `fAnchoM` (Float)
- Obligatorios — `required`
- Mayor que 0 — `@api.constrains`
- Como mucho 30 m — `@api.constrains`
- Como mucho dos decimales — `@api.constrains`

### `sTipo` (Selection)
- Lista cerrada: lona, valla, banderola, pantalla digital, photocall, mupi, vinilo de suelo — `fields.Selection`

### `sUbicacionExacta` (Char)
- Sin espacios sobrantes, entre 3 y 200 caracteres — `@api.constrains`

### `bIluminado` (Boolean)
- Sin validaciones.

### Relaciones
- `exhibicion_ids` (One2many → ExhibicionMarca) — exhibiciones que acoge (inverso de `espacio_publicitario_id`).

## Servicio (`feria.servicio`) — `servicio.py`

### `sCodigo` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`
- No vacío ni solo espacios — `@api.constrains`
- Entre 2 y 20 caracteres — `@api.constrains`
- Código en mayúsculas, sin espacios (ej. `SRV-SONIDO`) — `@api.constrains`

### `sNombre` (Char)
- Obligatorio — `required`
- No vacío ni solo espacios — `@api.constrains`
- Sin espacios al principio ni al final — `@api.constrains`
- Entre 2 y 100 caracteres — `@api.constrains`

### `sUnidadFacturacion` (Selection)
- Lista cerrada: por hora, por día, por evento, por unidad, por persona, por metro cuadrado, precio cerrado — `fields.Selection`

### `bRequiereTecnico` (Boolean)
- Sin validaciones.

### Relaciones
- `servicio_proveedor_ids` (One2many → ServicioProveedor) — proveedores que lo ofrecen con su tarifa (inverso de `servicio_id`).

## Tecnico (`feria.tecnico`) — `tecnico.py`

### `sEspecialidad` (Selection)
- Lista cerrada: electricidad, sonido, iluminación, montaje y estructuras, fontanería, climatización, gas — `fields.Selection`

### `sCodCarnetProfesional` (Char)
- Único entre técnicos — `_sql_constraints`
- Entre 4 y 20 caracteres — `@api.constrains`
- Código en mayúsculas, sin espacios (ej. `ELEC-12345`) — `@api.constrains`

### `dFechaCaducidadCarnet` (Date)
- Exige que haya código de carné — `@api.constrains`
- Entre el 01/01/1970 y 15 años después de hoy — `@api.constrains`
- Aviso en el formulario si el carné ya está caducado (no impide guardar) — `@api.onchange`

### Relaciones
- `exhibicion_ids` (One2many → ExhibicionMarca) — exhibiciones que actualiza (inverso de `tecnico_id`).

## ServicioProveedor (`feria.servicio_proveedor`) — `servicio_proveedor.py`

Clase de asociación de la relación N:M «ofrece» entre Servicio y Proveedor (tabla SERVICIO_PROVEEDOR del relacional).

### `fPrecioTarifa` (Float)
- No menor que 0 y como mucho 1.000.000 € — `@api.constrains`
- Como mucho dos decimales (céntimos) — `@api.constrains`

### Relaciones
- `servicio_id` (Many2one → Servicio) — obligatorio (`required`); si se borra el servicio se borran sus tarifas (`ondelete='cascade'`).
- `proveedor_id` (Many2one → Proveedor) — obligatorio (`required`); si se borra el proveedor se borran sus tarifas (`ondelete='cascade'`).
- Un proveedor solo tiene una tarifa por servicio — `_sql_constraints` `UNIQUE ("servicio_id", "proveedor_id")`.

---

# Notas sobre la documentación

Los diagramas (E-R, relacional y UML) mantienen los nombres originales de los atributos (`nombre`, `codigo_lugar`…). En el código llevan la notación húngara (`sNombre`, `sCodigoLugar`…), pero de momento los diagramas no se cambian.

Nota: los atributos `Decimal` del UML (`alto_m`, `ancho_m`) se guardan como `Float` en Odoo. No hace falta cambiar el diagrama.

Nota: `logotipo` de Marca es `Binary` en el UML y `fields.Image` en el código. `Image` es un `Binary` de Odoo especializado en imágenes (comprueba que el archivo sea una imagen y la reduce de tamaño), así que los dos tipos coinciden.

---

# Pendiente de revisar

- **Los modelos todavía no se cargan en Odoo.** `models/__init__.py` no importa esta carpeta (ni ninguna de las otras) y `security/ir.model.access.csv` no tiene permisos para estos modelos. Hasta que se añadan, nada de esto se puede probar en Odoo.
- **Diagramas.** En el código los campos de relación siguen la convención de Odoo que usa el profesor (`_id` / `_ids`), mientras que el relacional usa los nombres de las claves ajenas (`dni_proveedor`, `codigo_tipo_transaccion`…). Las claves ajenas compuestas del relacional se convierten en un único Many2one, porque Odoo enlaza por su `id` interno.
- **Modelo nuevo `servicio_proveedor.py`.** Cuando se añadan los imports, hay que incluirlo también. Es la clase de asociación ServicioProveedor del UML.
- **Revisar si el precio de tarifa debe ser obligatorio.** Ahora una tarifa se puede guardar sin precio. La validación de que no sea negativo no está en el cuadro de restricciones del E-R; si se quiere, se añade.
- **Técnico no tiene `_rec_name`.** En el desplegable de la exhibición aparecerá como «feria.tecnico,1». Se arreglará cuando herede de Persona.
- **Herencia de Persona (pendiente).** Según el UML, Tecnico es subtipo de Persona (`_inherits`). `socios/persona.py` todavía está vacío.
- **Revisar que la marca, el técnico y el espacio de una exhibición sean opcionales.** Así lo marcan el relacional (`NULL`) y el UML (0..1), pero una exhibición sin marca ni espacio tiene poco sentido. Si se hacen obligatorios, hay que cambiarlo también en los diagramas.
- **Validaciones con claves ajenas (pendientes):** una exhibición no se solapa con otra del mismo espacio publicitario.
- **Campos calculados (pendientes):** `superficie_m2` y el estado de la exhibición.
- **Relaciones con modelos de los compañeros (pendientes):** Marca ↔ Evento (PATROCINIO, con `importe_aportacion` y `tipo_aportacion`, otra clase de asociación); EspacioPublicitario → ZonaCaseta. Y al revés, Producto apunta a Marca; Incidencia y Actuacion a Servicio; Mantenimiento a Tecnico.
