# Lista de compras semanal — Piccor

Este modelo genera la lista de compras de la semana a partir de los menús.

## Cada semana
1. Crear `compras/semanas/AAAA-MM-DD.txt` (fecha del lunes) con los platos de cada día
   (mismo formato que `semanas/2026-11-23.txt`). Para que calcule cantidades: `Plato | porciones`.
2. Correr:
   ```bash
   python3 compras/generar_lista.py compras/semanas/AAAA-MM-DD.txt
   ```
3. Abrir `compras/listas/lista-compras-AAAA-MM-DD.xlsx`:
   - **Lista de compras**: consolidado por rubro (verdulería, carnicería, etc.) con casillero para tildar.
   - **Productos por día**: qué se usa cada día y en qué platos.
   - **Platos por día**: cada plato con sus productos.
   - **A revisar**: platos nuevos sin receta, feriados con platos, productos supuestos.

## Recetas
`compras/recetas.py` tiene qué productos lleva cada plato. Si aparece un plato nuevo,
el script lo marca como "Plato sin receta" y hay que agregarlo ahí.
Los productos marcados con `s(...)` no figuran en el texto del menú: son supuestos de
receta (ej. pan rallado en la milanesa) y salen resaltados en amarillo para confirmar.
