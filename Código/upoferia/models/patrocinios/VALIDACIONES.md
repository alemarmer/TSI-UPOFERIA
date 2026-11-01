# Validaciones del bloque Patrocinio y servicios

Todas las validaciones de esta lista están implementadas.

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

---

# Notas sobre la documentación

Los diagramas (E-R, relacional y UML) mantienen los nombres originales de los atributos (`nombre`, `codigo_lugar`…). En el código llevan la notación húngara (`sNombre`, `sCodigoLugar`…), pero de momento los diagramas no se cambian.

Nota: los atributos `Decimal` del UML (`alto_m`, `ancho_m`) se guardan como `Float` en Odoo. No hace falta cambiar el diagrama.

Nota: `logotipo` de Marca es `Binary` en el UML y `fields.Image` en el código. `Image` es un `Binary` de Odoo especializado en imágenes (comprueba que el archivo sea una imagen y la reduce de tamaño), así que los dos tipos coinciden.
