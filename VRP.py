import math
from operator import itemgetter

# Datos de coordenadas
coord = {
    'EDO.MEX': (19.2938258568844, -99.65366252023884),
    'QRO': (20.593537489366717, -100.39004057702225),
    'CDMX': (19.432854452264177, -99.13330004822943),
    'SLP': (22.151725492903953, -100.97657666103268),
    'MTY': (25.673156272083876, -100.2974200019319),
    'PUE': (19.063532268065185, -98.30729139446866),
    'GDL': (20.67714565083998, -103.34696388920293),
    'MICH': (19.702614895389996, -101.19228631929688),
    'SON': (29.075273188617818, -110.95962477655333)
}

# Datos de pedidos por ciudad
pedidos = {
    'EDO.MEX': 10,
    'QRO': 13,
    'CDMX': 7,
    'SLP': 11,
    'MTY': 15,
    'PUE': 8,
    'GDL': 6,
    'MICH': 7,
    'SON': 8
}

# Volumen de paquetes por ciudad
volumen_paquetes = {
    'EDO.MEX': 2,
    'QRO': 3,
    'CDMX': 1.5,
    'SLP': 2.5,
    'MTY': 4,
    'PUE': 2,
    'GDL': 1.8,
    'MICH': 2.2,
    'SON': 3.5
}

def distancia(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

def en_ruta(rutas, c):
    for r in rutas:
        if c in r:
            return r
    return None

def peso_ruta(ruta):
    return sum(pedidos[c] for c in ruta)

def volumen_ruta(ruta):
    return sum(volumen_paquetes[c] for c in ruta)

def distancia_ruta(ruta, almacen):
    total = distancia(almacen, coord[ruta[0]])
    for i in range(len(ruta) - 1):
        total += distancia(coord[ruta[i]], coord[ruta[i+1]])
    total += distancia(coord[ruta[-1]], almacen)
    return total

def consumo_gasolina(dist):
    return dist / 10

def vrp_voraz(ciudad_origen, ciudad_destino, max_carga, max_distancia, max_gasolina, max_volumen):
    almacen = coord[ciudad_origen]
    coord_filtradas = {k: v for k, v in coord.items() if k == ciudad_origen or k == ciudad_destino}

    s = {}
    for c1 in coord_filtradas:
        for c2 in coord_filtradas:
            if c1 != c2 and not (c2, c1) in s:
                d_c1_c2 = distancia(coord[c1], coord[c2])
                d_c1_almacen = distancia(coord[c1], almacen)
                d_c2_almacen = distancia(coord[c2], almacen)
                s[c1, c2] = d_c1_almacen + d_c2_almacen - d_c1_c2

    s = sorted(s.items(), key=itemgetter(1), reverse=True)
    rutas = []

    for k, v in s:
        rc1 = en_ruta(rutas, k[0])
        rc2 = en_ruta(rutas, k[1])

        if rc1 is None and rc2 is None:
            nueva_ruta = [k[0], k[1]]
            dist = distancia_ruta(nueva_ruta, almacen)
            gas = consumo_gasolina(dist)
            if (peso_ruta(nueva_ruta) <= max_carga and 
                dist <= max_distancia and
                gas <= max_gasolina and
                volumen_ruta(nueva_ruta) <= max_volumen):
                rutas.append(nueva_ruta)

    return rutas

# Exportamos variables para uso externo
__all__ = ["vrp_voraz", "coord", "pedidos", "volumen_paquetes", "distancia_ruta", "peso_ruta", "volumen_ruta", "consumo_gasolina"]


# Datos a tomar en cuenta para la api. Tiene que pedir como datos de entrada la ciudad de origen ( en donde se encuentra el almacen) y la ciudad de destino, el maximo de paquetes que se pueden llevar y el maximo de distancia que se puede recorrer y el maximo de gasolina que se puede consumir, todo esto dentro de un viaje.