"""Catálogo de productos y recetas de Piccor.

Cómo se lee:
- PRODUCTOS: cada producto con la categoría de compra (verdulería, carnicería, etc.).
- RECETAS: cada plato con sus productos.
    m("producto")  -> el producto figura en el texto del menú (dato).
    s("producto")  -> el producto NO figura en el texto; es una suposición de
                      receta (ej. pan rallado en una milanesa). En la lista sale
                      marcado como "supuesto" para que lo confirmes.
  Opcional: cantidad por porción, ej. m("papa", 0.25, "kg"). Si se cargan
  cantidades por porción y en el menú semanal se indica cuántas porciones
  ("Plato | 20"), el script calcula cuánto comprar.
- ALIAS: el primer texto es el nombre "oficial" del plato; los demás son
  otras formas en que aparece escrito en los menús.
"""

VERDU = "Verdulería"
CARNE = "Carnicería / Pollería"
FIAMB = "Fiambrería / Lácteos / Huevos"
ALMA = "Almacén"
PANA = "Panadería / Masas"

PRODUCTOS = {
    # Verdulería
    "hojas verdes / lechuga": VERDU, "tomate": VERDU, "tomate cherry": VERDU,
    "zanahoria": VERDU, "cebolla": VERDU, "cebolla morada": VERDU,
    "cebolla de verdeo": VERDU, "puerro": VERDU, "zapallito": VERDU,
    "calabaza": VERDU, "batata": VERDU, "papa": VERDU, "brócoli": VERDU,
    "repollo": VERDU, "pepino": VERDU, "remolacha": VERDU, "morrón": VERDU,
    "choclo": VERDU, "hongos": VERDU, "perejil": VERDU, "albahaca": VERDU,
    "ajo": VERDU, "verduras para salteado (a definir)": VERDU,
    # Carnicería / Pollería
    "pechuga de pollo": CARNE, "pata y muslo": CARNE, "pollo (para asar / grillar)": CARNE,
    "carne para milanesa": CARNE, "carne para brasear (corte a definir)": CARNE,
    "ternera (corte a definir)": CARNE, "costillas de cerdo / ribs": CARNE,
    "bondiola de cerdo": CARNE,
    # Fiambrería / Lácteos / Huevos
    "huevos": FIAMB, "queso (barra / muzzarella)": FIAMB, "queso azul": FIAMB,
    "queso parmesano / rallado": FIAMB, "jamón cocido": FIAMB, "salame": FIAMB,
    "leche": FIAMB, "crema de leche": FIAMB, "manteca": FIAMB,
    # Almacén
    "arroz blanco": ALMA, "arroz yamaní": ALMA, "lentejas": ALMA, "azafrán": ALMA,
    "fideos": ALMA, "fideos integrales": ALMA, "ñoquis (o papa + harina)": ALMA,
    "harina": ALMA, "harina integral": ALMA, "pan rallado": ALMA,
    "mayonesa": ALMA, "aderezo césar": ALMA, "salsa barbacoa": ALMA,
    "tomate triturado / puré de tomate": ALMA, "tomates secos": ALMA,
    "atún": ALMA, "aceitunas": ALMA, "maní": ALMA, "sésamo": ALMA,
    "vinagre": ALMA, "aceite": ALMA,
    # Panadería / Masas
    "pan para sándwich": PANA, "pan integral": PANA, "pan para crutones": PANA,
    "tortillas para tacos": PANA, "tapas de empanada": PANA,
    "masa para tarta integral": PANA, "masa para strudel / hojaldre": PANA,
    "masa para canelones / panqueques": PANA, "masa para tequeños": PANA,
}


def m(producto, cant=None, unidad=None):
    return {"producto": producto, "supuesto": False, "cant": cant, "unidad": unidad}


def s(producto, cant=None, unidad=None):
    return {"producto": producto, "supuesto": True, "cant": cant, "unidad": unidad}


# Bloques que se repiten
PICKLES = [m("cebolla"), s("vinagre")]
CRUTONES = [m("pan para crutones")]
MAYO_ALBAHACA = [m("mayonesa"), m("albahaca")]
PESTO = [m("albahaca"), s("ajo"), s("aceite")]
ALIOLI = [s("ajo"), s("mayonesa")]
MILANESA_CARNE = [m("carne para milanesa"), s("pan rallado"), s("huevos")]
MILANESA_POLLO = [m("pechuga de pollo"), s("pan rallado"), s("huevos")]
SALSA_BLANCA = [s("leche"), s("manteca"), s("harina")]
PAPAS_HORNO = [m("papa")]
CESAR = [m("hojas verdes / lechuga"), m("queso parmesano / rallado"), m("pan para crutones"), m("aderezo césar")]
ENS_ARROZ_LENTEJAS = [m("arroz blanco"), m("lentejas"), m("calabaza"), m("tomate cherry")]
ENS_HOJAS_LENTEJA = [m("hojas verdes / lechuga"), m("lentejas"), m("zanahoria"), m("cebolla morada"), m("pepino")]
ENS_PARMA = [m("hojas verdes / lechuga"), m("lentejas"), m("zanahoria"), m("tomate cherry"),
             m("queso parmesano / rallado"), m("aderezo césar")]
ENS_VEGETARIANA = [m("hojas verdes / lechuga"), m("lentejas"), m("calabaza"), m("tomate cherry"), *PICKLES]
ENS_TRICOLOR = [m("arroz yamaní"), m("zanahoria"), m("choclo"), m("huevos")]
ENS_GENERICA = [s("hojas verdes / lechuga"), s("tomate")]  # "ensalada" sin detalle


RECETAS = [
    # ---------- Menú del día 23-27/11 (flyer) ----------
    (["Poke bowl: base de hojas, croquetas de lentejas, calabaza asada, pickles de cebolla, queso en cubos, tomate cherry y crutones con alioli de remolacha",
      "Poke Bowl Base de hojas croquetas de lentejas,calabaza azada,pickles de cebolla,queso en cubos tomate Cherry crutones cOn alioli de remolacha"],
     [m("hojas verdes / lechuga"), m("lentejas"), s("pan rallado"), m("calabaza"), *PICKLES,
      m("queso (barra / muzzarella)"), m("tomate cherry"), *CRUTONES, m("remolacha"), *ALIOLI]),
    (["Milanesa suprema con salteado de arroz, verduras y azafrán",
      "Milansea suprema con salteado de arroz verduras y azafran"],
     [*MILANESA_POLLO, m("arroz blanco"), m("verduras para salteado (a definir)"), m("azafrán")]),
    (["Strudel integral relleno de brócoli, puerro y queso azul con ensalada de papa y huevo",
      "Strudel integral relleno de brocoli puerro queso azul con ensalada de papa y huevo"],
     [m("masa para strudel / hojaldre"), s("harina integral"), m("brócoli"), m("puerro"), m("queso azul"),
      m("papa"), m("huevos")]),
    (["Tacos de carne braseada, repollo y mayo de albahaca con batata y zanahoria al horno",
      "Tacos de carne braseada repollo mayo de alabahaca con batata y zanahoria al horno"],
     [m("tortillas para tacos"), m("carne para brasear (corte a definir)"), m("repollo"), *MAYO_ALBAHACA,
      m("batata"), m("zanahoria")]),
    (["Tarta integral de puerro, cebolla y zapallito con queso, ensalada de papa, cebolla morada, perejil y huevo con mayonesa",
      "Tarta integral de puerro cebolla y zapallito con queso,ensalada de papa cebolla morada perejil y huevo con mayonesa"],
     [m("masa para tarta integral"), m("puerro"), m("cebolla"), m("zapallito"), m("queso (barra / muzzarella)"),
      m("papa"), m("cebolla morada"), m("perejil"), m("huevos"), m("mayonesa")]),
    (["Ribs de cerdo a la barbacoa con ensalada de hojas, crutones, zanahoria, choclo y tomate",
      "Ribs de cerdo a la barbacoa con ensalada hojas crutones zanahoria choclo y tomate"],
     [m("costillas de cerdo / ribs"), m("salsa barbacoa"), m("hojas verdes / lechuga"), *CRUTONES,
      m("zanahoria"), m("choclo"), m("tomate")]),
    (["Salteado de fideos integrales con brócoli, cherry asado, pesto y hongos con sésamo y perejil fresco",
      "Salteado de fideos integrales con brocoli Cherry asado pesto y hongos con sesamo y perejil fresco"],
     [m("fideos integrales"), m("brócoli"), m("tomate cherry"), *PESTO, m("hongos"), m("sésamo"), m("perejil")]),
    (["Sándwich de ternera grillado con pesto, alioli, queso, tomate y lechuga con papas bastón",
      "Sandwich de ternera grillado pesto alioli queso tomate y lechuga con papas baston"],
     [m("pan para sándwich"), m("ternera (corte a definir)"), *PESTO, *ALIOLI, m("queso (barra / muzzarella)"),
      m("tomate"), m("hojas verdes / lechuga"), m("papa"), s("aceite")]),

    # ---------- Platos de la carta / pedidos ----------
    (["Sandwich integral de pollo grillado con pesto de tomate,queso,lechuga,y papas al horno"],
     [m("pan integral"), m("pechuga de pollo"), s("tomates secos"), s("aceite"), m("queso (barra / muzzarella)"),
      m("hojas verdes / lechuga"), *PAPAS_HORNO]),
    (["Sandwich de Milanesa de carne"],
     [m("pan para sándwich"), *MILANESA_CARNE]),
    (["Sandwich de milanesa completo con papas al horno"],
     # "completo": se supone lechuga, tomate, jamón, queso y huevo
     [m("pan para sándwich"), *MILANESA_CARNE, s("hojas verdes / lechuga"), s("tomate"), s("jamón cocido"),
      s("queso (barra / muzzarella)"), *PAPAS_HORNO]),
    (["Canelones de jamon y queso con salsa blanca y salsa de tomate."],
     [s("masa para canelones / panqueques"), m("jamón cocido"), m("queso (barra / muzzarella)"), *SALSA_BLANCA,
      s("tomate triturado / puré de tomate")]),
    (["3 Empanadas de humita calabaza y queso con ensalada de hojas crotones huevo y calabaza asada"],
     [m("tapas de empanada"), s("choclo"), m("calabaza"), m("queso (barra / muzzarella)"),
      m("hojas verdes / lechuga"), *CRUTONES, m("huevos")]),
    (["Ensalada: arroz blanco,lentejas,calabaza horneada ,tomate cherry, pollo"],
     [*ENS_ARROZ_LENTEJAS, m("pollo (para asar / grillar)")]),
    (["Ensalada: arroz blanco,lentejas,calabaza horneada ,tomate cherry, atun"],
     [*ENS_ARROZ_LENTEJAS, m("atún")]),
    (["Ensalada: Hojas lenteja zanahoria cebolla morada y pepino atun"],
     [*ENS_HOJAS_LENTEJA, m("atún")]),
    (["Ensalada: Parma: Hojas, lentejas, zanahoria en cubos hervida, cherri, pollo, queso parmesado, aderezo cesar."],
     [*ENS_PARMA, m("pollo (para asar / grillar)")]),
    (["Ensalada: Parma:Hojas,lentejas,zanahoria en cubos hervida,cherri,atun ,queso parmesado,aderezo cesar."],
     [*ENS_PARMA, m("atún")]),
    (["Ensalada: vegetariana:Hojas verdes,lentejas,calabaza asada,tomates cherrys confitados,pickles de Cebolla"],
     ENS_VEGETARIANA),
    (["Ens veg:Hojas verdes,lentejas,calabaza asada,cherrys confi,pickles de Cebolla y atun"],
     [*ENS_VEGETARIANA, m("atún")]),
    (["Ensalada: Tricolor:Yamani,zanahoria rallada,choclo y huevo duro, atun"],
     [*ENS_TRICOLOR, m("atún")]),
    (["Ensalada: Tricolor:Yamani,zanahoria rallada,choclo y huevo duro, pollo"],
     [*ENS_TRICOLOR, m("pollo (para asar / grillar)")]),
    (["Ensalada: Caesar con lentejas"], [*CESAR, m("lentejas")]),
    (["Ensalada: Caesar con pollo"], [*CESAR, m("pollo (para asar / grillar)")]),
    (["Ensalada: Cesar,hojas parmesano,crutones,pollo asado y aderezo con atun"],
     [*CESAR, m("pollo (para asar / grillar)"), m("atún")]),
    (["Milanesa de pollo a la napolitana con pure de papas"],
     [*MILANESA_POLLO, s("jamón cocido"), s("queso (barra / muzzarella)"), s("tomate triturado / puré de tomate"),
      m("papa"), s("leche"), s("manteca")]),
    (["Pata y muslo con 2 huevos"], [m("pata y muslo"), m("huevos")]),
    (["Pata y muslo con arroz"], [m("pata y muslo"), m("arroz blanco")]),
    (["Pata y muslo con ensalada."], [m("pata y muslo"), *ENS_GENERICA]),
    (["Sandwich de jamon y queso"], [m("pan para sándwich"), m("jamón cocido"), m("queso (barra / muzzarella)")]),
    (["Sandwich de salame y queso"], [m("pan para sándwich"), m("salame"), m("queso (barra / muzzarella)")]),
    (["Croqueta de arroz rellena de queso rebozada al horno con ensalada mix de hojas pickles de cebolla tomate zanahoria rallada"],
     [m("arroz blanco"), m("queso (barra / muzzarella)"), s("pan rallado"), s("huevos"),
      m("hojas verdes / lechuga"), *PICKLES, m("tomate"), m("zanahoria")]),
    (["Sandwich de pollo frito con (ens coleslaw con mayonesa) con papas al horno."],
     # coleslaw: se supone repollo y zanahoria
     [m("pan para sándwich"), m("pechuga de pollo"), s("harina"), s("pan rallado"), s("huevos"), s("aceite"),
      s("repollo"), s("zanahoria"), m("mayonesa"), *PAPAS_HORNO]),
    (["Miloja de papas a la crema con ensalada de arroz con mayonesa aceitunas tomate y perejil"],
     [m("papa"), m("crema de leche"), s("queso (barra / muzzarella)"), m("arroz blanco"), m("mayonesa"),
      m("aceitunas"), m("tomate"), m("perejil")]),
    (["Tacos de bondiola con repollo y mayo de albahaca papas al horno."],
     [m("tortillas para tacos"), m("bondiola de cerdo"), m("repollo"), *MAYO_ALBAHACA, *PAPAS_HORNO]),
    (["Costillas de cerdo con arroz al azafran cremoso cebolla morron y verdeo."],
     [m("costillas de cerdo / ribs"), m("arroz blanco"), m("azafrán"), s("crema de leche"), m("cebolla"),
      m("morrón"), m("cebolla de verdeo")]),
    (["Tequeños al horno con mayo de albahaca papas al horno y ensalada."],
     [s("masa para tequeños"), s("queso (barra / muzzarella)"), *MAYO_ALBAHACA, *PAPAS_HORNO, *ENS_GENERICA]),
    (["Fideos al pesto con pollo y queso rallado"],
     [m("fideos"), *PESTO, m("pollo (para asar / grillar)"), m("queso parmesano / rallado")]),
    (["Ñoquis con crema de calabaza,brocoli y mani,con queso."],
     [s("ñoquis (o papa + harina)"), m("calabaza"), s("crema de leche"), m("brócoli"), m("maní"),
      m("queso (barra / muzzarella)")]),
]
