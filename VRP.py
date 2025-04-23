import math
from operator import itemgetter

def distancia(coord1, coord2):
    lat1 = coord1[0]
    lon1 = coord1[1]
    lat2 = coord2[0]
    lon2 = coord2[1]
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def en_ruta(rutas, c):
    ruta = None
    for r in rutas:
        if c in r:
            ruta = r
    return ruta

def peso_ruta(ruta):
    total = 0
    for c in ruta:
        total += pedidos[c]
    return total

def distancia_ruta(ruta):
    total = distancia(almacen, coord[ruta[0]])
    for i in range(len(ruta)-1):
        total += distancia(coord[ruta[i]], coord[ruta[i+1]])
    total += distancia(coord[ruta[-1]], almacen)
    return total

def consumo_gasolina(distancia):
    # Suponiendo un consumo de 10 km por litro (puede ajustarse)
    return distancia / 10

# INICIO DE LA FUNCIÓN VRP
def vrp_voraz():
    # Calcular los ahorros
    s = {}
    for c1 in coord:
        for c2 in coord:
            if c1 != c2:
                if not (c2, c1) in s:
                    d_c1_c2 = distancia(coord[c1], coord[c2])
                    d_c1_almacen = distancia(coord[c1], almacen)
                    d_c2_almacen = distancia(coord[c2], almacen)
                    s[c1, c2] = d_c1_almacen + d_c2_almacen - d_c1_c2
    # Ordenar ahorros
    s = sorted(s.items(), key=itemgetter(1), reverse=True)

    # Construir rutas
    rutas = []
    for k, v in s:
        rc1 = en_ruta(rutas, k[0])
        rc2 = en_ruta(rutas, k[1])
        
        # Verificar restricciones para cada caso
        if rc1 == None and rc2 == None:
            # No están en ninguna Ruta, la creamos
            nueva_ruta = [k[0], k[1]]
            if (peso_ruta(nueva_ruta) <= max_carga and 
                distancia_ruta(nueva_ruta) <= max_distancia and
                consumo_gasolina(distancia_ruta(nueva_ruta)) <= max_gasolina):
                rutas.append(nueva_ruta)
                
        elif rc1 != None and rc2 == None:
            # Cliente 1 ya está en una ruta, agregamos cliente 2
            if rc1[0] == k[0]:
                nueva_ruta = [k[1]] + rc1
            elif rc1[-1] == k[0]:
                nueva_ruta = rc1 + [k[1]]
            else:
                continue
                
            if (peso_ruta(nueva_ruta) <= max_carga and 
                distancia_ruta(nueva_ruta) <= max_distancia and
                consumo_gasolina(distancia_ruta(nueva_ruta)) <= max_gasolina):
                rutas[rutas.index(rc1)] = nueva_ruta
                
        elif rc1 == None and rc2 != None:
            # Cliente 2 ya está en una ruta, agregamos cliente 1
            if rc2[0] == k[1]:
                nueva_ruta = [k[0]] + rc2
            elif rc2[-1] == k[1]:
                nueva_ruta = rc2 + [k[0]]
            else:
                continue
                
            if (peso_ruta(nueva_ruta) <= max_carga and 
                distancia_ruta(nueva_ruta) <= max_distancia and
                consumo_gasolina(distancia_ruta(nueva_ruta)) <= max_gasolina):
                rutas[rutas.index(rc2)] = nueva_ruta
                
        elif rc1 != None and rc2 != None and rc1 != rc2:
            # Unir dos rutas existentes
            if rc1[0] == k[0] and rc2[-1] == k[1]:
                nueva_ruta = rc2 + rc1
            elif rc1[-1] == k[0] and rc2[0] == k[1]:
                nueva_ruta = rc1 + rc2
            else:
                continue
                
            if (peso_ruta(nueva_ruta) <= max_carga and 
                distancia_ruta(nueva_ruta) <= max_distancia and
                consumo_gasolina(distancia_ruta(nueva_ruta)) <= max_gasolina):
                rutas.remove(rc1)
                rutas.remove(rc2)
                rutas.append(nueva_ruta)
                
    return rutas

if __name__ == "__main__":
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

    almacen = (19.432854452264177, -99.13330004822943)
    max_carga = 40
    max_distancia = 5  # Nueva dimensión: distancia máxima por ruta (en unidades de distancia)
    max_gasolina = 12  # Nueva dimensión: máximo de litros de gasolina por ruta

    rutas = vrp_voraz()
    
    print("Rutas generadas:")
    for i, ruta in enumerate(rutas, 1):
        dist = distancia_ruta(ruta)
        gas = consumo_gasolina(dist)
        print(f"Ruta {i}: {ruta}")
        print(f"  - Peso total: {peso_ruta(ruta)}/{max_carga} de paquetes")
        print(f"  - Distancia total: {dist:.2f}/{max_distancia} km")
        print(f"  - Consumo gasolina: {gas:.2f}L/{max_gasolina} Lts\n")

# Datos a tomar en cuenta para la api. Tiene que pedir como datos de entrada la ciudad de origen ( en donde se encuentra el almacen) y la ciudad de destino, el maximo de paquetes que se pueden llevar y el maximo de distancia que se puede recorrer y el maximo de gasolina que se puede consumir, todo esto dentro de un viaje.

# TODO: Agregar dos dimensiónes más (distancia, caseta, hrs trabajadas, etc) en API
# donde estas, done esta tu almacen, etc.