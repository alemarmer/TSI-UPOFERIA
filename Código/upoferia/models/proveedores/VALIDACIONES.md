## CategoriaProveedor (`feria.categoria_proveedor`) — `categoria_proveedor.py`

### `sNombre` (Char) — clave
- Obligatorio — `required`
- Único — `_sql_constraints`
- No vacío ni solo espacios — `@api.constrains`
- Sin espacios al principio ni al final — `@api.constrains`
- Entre 2 y 50 caracteres — `@api.constrains`
- Único sin distinguir mayúsculas («Catering» = «CATERING») — `@api.constrains`

### `iColor` (Integer)
- Número entre 0 y 11 (la paleta de colores de las etiquetas de Odoo); por defecto 0 — `@api.constrains`

## Proveedor (`feria.proveedor`) — `proveedor.py`

### `sCif` (Char)
- Único — `_sql_constraints`
- Una letra mayúscula, 7 dígitos y un carácter de control, sin espacios (ej. `B12345674`) — `@api.constrains`
- Carácter de control correcto según el algoritmo oficial del CIF — `@api.constrains`

---

# Notas sobre la documentación

Los diagramas (E-R, relacional y UML) mantienen los nombres originales de los atributos (`nombre`, `color`, `cif`). En el código llevan la notación húngara (`sNombre`, `iColor`, `sCif`), pero de momento los diagramas no se cambian.
