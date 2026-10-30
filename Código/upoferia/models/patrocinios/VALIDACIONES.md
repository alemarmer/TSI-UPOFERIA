# Validaciones del bloque Patrocinio y servicios

Todas las validaciones de esta lista están implementadas.

## Marca (`feria.marca`) — `marca.py`

### `sNombre` (Char) — clave
- Obligatorio — `required`
- Único — `_sql_constraints`
- No vacío ni solo espacios — `@api.constrains`
- Sin espacios al principio ni al final — `@api.constrains`
- Entre 2 y 100 caracteres — `@api.constrains`

### `sLogotipo` (Char)
- Sin espacios — `@api.constrains`
- Como mucho 255 caracteres — `@api.constrains`

### `sColorCorporativo` (Char)
- Formato `#RRGGBB` o `#RGB` — `@api.constrains`

**Pendiente (fase de relaciones)**
- `dni_proveedor` → `Many2one` opcional a PROVEEDOR.

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

**Pendiente (fase de relaciones)**
- Claves ajenas a MARCA, TECNICO y ESPACIO_PUBLICITARIO.
- No solaparse con otra exhibición del mismo espacio.
- Estado calculado a partir de las fechas.

## EspacioPublicitario (`feria.espacio_publicitario`) — `espacio_publicitario.py`

### `sCodigoLugar` (Char) — clave
- Obligatorio y único — `required` / `_sql_constraints`
- No vacío ni solo espacios — `@api.constrains`
- Entre 2 y 20 caracteres — `@api.constrains`
- Código en mayúsculas, sin espacios (ej. `PORTADA-01`) — `@api.constrains`

### `fAltoM` y `fAnchoM` (Float)
- Mayor que 0 — `@api.constrains`
- Como mucho 30 m — `@api.constrains`
- Como mucho dos decimales — `@api.constrains`

### `sTipo` (Char)
- Sin espacios sobrantes, entre 2 y 50 caracteres — `@api.constrains`

### `sUbicacionExacta` (Char)
- Sin espacios sobrantes, entre 3 y 200 caracteres — `@api.constrains`

### `bIluminado` (Boolean)
- Sin validaciones.

**Pendiente (fase de relaciones)**
- Clave ajena a ZONA_CASETA.
- `fSuperficieM2 = fAnchoM × fAltoM` como campo calculado.

---

# Cambios que hay que hacer en la documentación

## Por qué
En Odoo, el nombre del campo es el nombre de la columna en la base de datos. Al cambiar los nombres a la notación del profesor, los diagramas dejan de coincidir con el código.

## 1. Renombrar atributos en el E-R, el relacional y el UML

| Clase | E-R / relacional | UML | Nombre nuevo |
|---|---|---|---|
| Marca | `nombre` | `nombre` | `sNombre` |
| Marca | `logotipo` | `logotipo` | `sLogotipo` |
| Marca | `color_corporativo` | `colorCorporativo` | `sColorCorporativo` |
| ExhibicionMarca | `id_exhibicion` | `idExhibicion` | `sIdExhibicion` |
| ExhibicionMarca | `fecha_montaje` | `fechaMontaje` | `dFechaMontaje` |
| ExhibicionMarca | `arte_final` | `arteFinal` | `sArteFinal` |
| ExhibicionMarca | `fecha_retirada` | `fechaRetirada` | `dFechaRetirada` |
| EspacioPublicitario | `codigo_lugar` | `codigoLugar` | `sCodigoLugar` |
| EspacioPublicitario | `alto_m` | `altoM` | `fAltoM` |
| EspacioPublicitario | `tipo` | `tipo` | `sTipo` |
| EspacioPublicitario | `ubicacion_exacta` | `ubicacionExacta` | `sUbicacionExacta` |
| EspacioPublicitario | `ancho_m` | `anchoM` | `fAnchoM` |
| EspacioPublicitario | `iluminado` | `iluminado` | `bIluminado` |
| EspacioPublicitario | `superficie_m2` | `/superficieM2` | `fSuperficieM2` |

Prefijos: `s` texto, `d` fecha, `f` decimal, `b` sí/no.

## 2. Otras páginas donde aparecen esos nombres
- Relacional, página «Notación textual y decisiones»: líneas de MARCA, EXHIBICION_MARCA y ESPACIO_PUBLICITARIO.
- UML, página «Trazabilidad tablas → UML»: los mismos tres apartados.
- E-R, cuadro de restricciones:
  - `fecha_retirada ≥ fecha_montaje` → `dFechaRetirada ≥ dFechaMontaje`
  - `superficie_m2 = ancho_m × alto_m` → `fSuperficieM2 = fAnchoM × fAltoM`

## 3. Claves ajenas que apuntan a estas tablas (revisar con el grupo)

| Tabla | Columna actual | Columna nueva |
|---|---|---|
| PRODUCTO | `nombre_marca` | `sNombreMarca` |
| EXHIBICION_MARCA | `nombre_marca` | `sNombreMarca` |
| PATROCINIO | `nombre_marca` | `sNombreMarca` |
| EXHIBICION_MARCA | `codigo_lugar_espacio_publicitario` | `sCodigoLugarEspacioPublicitario` |

PRODUCTO es de otro bloque: hay que avisar a quien lo lleve. En el código no se rompe nada, porque serán `Many2one`.

## 4. Reglas que se pueden añadir al cuadro de restricciones del E-R (opcional)
- EXHIBICION_MARCA:
  - no hay fecha de retirada sin fecha de montaje;
  - dura como mucho un año;
  - el montaje es como mucho a dos años vista.
- ESPACIO_PUBLICITARIO: alto y ancho entre 0 y 30 metros.

## 5. Pendiente de decidir en el grupo
- `sTipo`: el E-R dice que es una lista cerrada, pero no da los valores. De momento es texto libre.
- `sLogotipo` y `sArteFinal`: guardan una URL o una ruta (`String` en el UML). Si se quiere subir el archivo, habría que pasarlos a `Binary`.
- `Decimal` del UML se guarda como `Float` en Odoo. No hace falta cambiar el diagrama.
