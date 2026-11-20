#!/usr/bin/env python3
"""Genera la lista de compras semanal de Piccor a partir del menú de la semana.

Uso:
    python3 compras/generar_lista.py compras/semanas/2026-11-23.txt

Formato del archivo de la semana (texto plano):
    Lunes 23 de noviembre          <- encabezado de día
    Nombre del plato               <- un plato por línea
    Nombre del plato | 20          <- opcional: porciones
    FERIADO                        <- marca el día como feriado
    # comentario                   <- se ignora
Líneas "Menú" y "Total general del día" se ignoran. Los platos antes del
primer día quedan en "Sin día asignado".

Salida: compras/listas/lista-compras-<nombre>.xlsx
"""
import difflib
import re
import sys
import unicodedata
from collections import OrderedDict
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

sys.path.insert(0, str(Path(__file__).parent))
from recetas import PRODUCTOS, RECETAS  # noqa: E402

DIAS = ("lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo")
ORDEN_CATEGORIAS = ["Verdulería", "Carnicería / Pollería", "Fiambrería / Lácteos / Huevos",
                    "Almacén", "Panadería / Masas"]
SIN_DIA = "Sin día asignado"


def norm(t):
    t = unicodedata.normalize("NFKD", t.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r"[^a-z0-9ñ ]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def indice_recetas():
    errores = []
    idx = {}
    for alias, ings in RECETAS:
        for a in alias:
            idx[norm(a)] = (alias[0], ings)
        for i in ings:
            if i["producto"] not in PRODUCTOS:
                errores.append(f"'{i['producto']}' (plato: {alias[0]}) no está en PRODUCTOS")
    if errores:
        sys.exit("Errores en recetas.py:\n  " + "\n  ".join(errores))
    return idx


def leer_semana(path):
    dias = OrderedDict()
    actual = SIN_DIA
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        linea = raw.strip()
        if not linea or linea.startswith("#"):
            continue
        n = norm(linea)
        if n in ("menu", "total general del dia"):
            continue
        if n.split(" ")[0] in DIAS and re.search(r"\d", n):
            actual = linea
            dias.setdefault(actual, {"platos": [], "feriado": False})
            continue
        dias.setdefault(actual, {"platos": [], "feriado": False})
        if n == "feriado":
            dias[actual]["feriado"] = True
            continue
        porciones = None
        if "|" in linea:
            linea, p = linea.rsplit("|", 1)
            linea = linea.strip()
            porciones = float(p.strip().replace(",", ".")) if p.strip() else None
        dias[actual]["platos"].append((linea, porciones))
    return dias


def buscar(idx, plato):
    n = norm(plato)
    if n in idx:
        return idx[n], None
    cerca = difflib.get_close_matches(n, list(idx), n=1, cutoff=0.85)
    if cerca:
        return idx[cerca[0]], idx[cerca[0]][0]
    return None, None


def main(path):
    idx = indice_recetas()
    semana = leer_semana(path)
    revisar = []
    platos_dia = []          # (dia, plato_oficial, porciones, ingredientes)
    for dia, d in semana.items():
        if d["feriado"] and d["platos"]:
            revisar.append(("Feriado con platos", dia,
                            "El día está marcado FERIADO pero tiene platos cargados: se incluyeron igual."))
        if dia == SIN_DIA and d["platos"]:
            revisar.append(("Sin día", dia, "Estos platos no tienen día: se incluyeron en la lista general."))
        for plato, porc in d["platos"]:
            rec, aprox = buscar(idx, plato)
            if rec is None:
                revisar.append(("Plato sin receta", dia, f"{plato} -> agregar a recetas.py"))
                platos_dia.append((dia, plato, porc, None))
                continue
            if aprox:
                revisar.append(("Coincidencia aproximada", dia, f"'{plato}' se tomó como '{aprox}'"))
            platos_dia.append((dia, rec[0], porc, rec[1]))

    # Consolidado por producto
    cons = {}
    por_dia = OrderedDict()
    for dia, plato, porc, ings in platos_dia:
        if not ings:
            continue
        vistos = set()
        for i in ings:
            p = i["producto"]
            c = cons.setdefault(p, {"dias": [], "platos": set(), "solo_supuesto": True,
                                    "cant": 0.0, "unidad": None, "cant_completa": True})
            if dia not in c["dias"]:
                c["dias"].append(dia)
            c["platos"].add(plato)
            c["solo_supuesto"] &= i["supuesto"]
            if p not in vistos:
                if i["cant"] is not None and porc:
                    c["cant"] += i["cant"] * porc
                    c["unidad"] = i["unidad"]
                else:
                    c["cant_completa"] = False
            vistos.add(p)
            pd = por_dia.setdefault(dia, OrderedDict()).setdefault(p, {"platos": [], "supuesto": True})
            if plato not in pd["platos"]:
                pd["platos"].append(plato)
            pd["supuesto"] &= i["supuesto"]

    wb = Workbook()
    azul = "2E388A"
    head_font = Font(bold=True, color="FFFFFF")
    head_fill = PatternFill("solid", fgColor=azul)
    cat_fill = PatternFill("solid", fgColor="F58220")
    sup_fill = PatternFill("solid", fgColor="FFF2CC")
    thin = Side(style="thin", color="BBBBBB")
    borde = Border(top=thin, bottom=thin, left=thin, right=thin)

    def hoja(ws, titulo, cols, anchos):
        ws.append([titulo])
        ws["A1"].font = Font(bold=True, size=14, color=azul)
        ws.append([f"Semana: {Path(path).stem}"])
        ws.append([])
        ws.append(cols)
        for c in ws[4]:
            c.font, c.fill, c.border = head_font, head_fill, borde
        for i, w in enumerate(anchos):
            ws.column_dimensions[chr(65 + i)].width = w
        ws.freeze_panes = "A5"

    def fila(ws, vals, fill=None):
        ws.append(vals)
        for c in ws[ws.max_row]:
            c.border = borde
            c.alignment = Alignment(wrap_text=True, vertical="top")
            if fill:
                c.fill = fill

    # Hoja 1: lista de compras
    ws = wb.active
    ws.title = "Lista de compras"
    hoja(ws, "Piccor — Lista de compras",
         ["✓", "Producto", "Cantidad a comprar", "Unidad", "Días que se usa", "Platos distintos", "Nota"],
         [5, 34, 18, 10, 44, 16, 40])
    for cat in ORDEN_CATEGORIAS:
        prods = sorted(p for p in cons if PRODUCTOS[p] == cat)
        if not prods:
            continue
        ws.append(["", cat])
        for c in ws[ws.max_row]:
            c.font, c.fill = Font(bold=True, color="FFFFFF"), cat_fill
        for p in prods:
            c = cons[p]
            cant = round(c["cant"], 2) if c["cant_completa"] and c["cant"] else ""
            nota = "Supuesto por receta: confirmar" if c["solo_supuesto"] else ""
            fila(ws, ["☐", p, cant, c["unidad"] or "", ", ".join(c["dias"]), len(c["platos"]), nota],
                 sup_fill if c["solo_supuesto"] else None)

    # Hoja 2: productos por día
    ws = wb.create_sheet("Productos por día")
    hoja(ws, "Productos por día", ["Día", "Categoría", "Producto", "Platos que lo usan", "Nota"],
         [26, 26, 34, 80, 28])
    for dia, prods in por_dia.items():
        orden = sorted(prods, key=lambda p: (ORDEN_CATEGORIAS.index(PRODUCTOS[p]), p))
        for p in orden:
            v = prods[p]
            fila(ws, [dia, PRODUCTOS[p], p, " / ".join(v["platos"]), "Supuesto" if v["supuesto"] else ""],
                 sup_fill if v["supuesto"] else None)

    # Hoja 3: platos por día
    ws = wb.create_sheet("Platos por día")
    hoja(ws, "Platos por día", ["Día", "Plato", "Porciones", "Productos"], [26, 70, 11, 90])
    for dia, plato, porc, ings in platos_dia:
        prods = ", ".join(dict.fromkeys(i["producto"] + (" (sup.)" if i["supuesto"] else "") for i in ings)) \
            if ings else "SIN RECETA"
        fila(ws, [dia, plato, porc or "", prods])

    # Hoja 4: a revisar
    ws = wb.create_sheet("A revisar")
    hoja(ws, "Para revisar antes de comprar", ["Tipo", "Día", "Detalle"], [26, 28, 100])
    fila(ws, ["Cantidades", "Toda la semana",
              "No hay porciones ni gramajes cargados: la columna 'Cantidad a comprar' queda vacía. "
              "Cargá porciones por plato ('Plato | 20') y cantidades por porción en recetas.py para calcularla."])
    for r in revisar:
        fila(ws, list(r))
    sup = sorted(p for p in cons if cons[p]["solo_supuesto"])
    if sup:
        fila(ws, ["Productos supuestos", "Toda la semana",
                  "No figuran en el texto del menú, se agregaron por receta: " + ", ".join(sup)])

    out = Path(__file__).parent / "listas" / f"lista-compras-{Path(path).stem}.xlsx"
    out.parent.mkdir(exist_ok=True)
    wb.save(out)
    print(f"Lista generada: {out}")
    print(f"Platos: {len(platos_dia)} | Productos: {len(cons)} | A revisar: {len(revisar)}")
    for r in revisar:
        print("  -", " | ".join(r))
    return out


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
