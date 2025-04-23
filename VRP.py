import math

# Coordenadas de las ciudades
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

def distancia(c1, c2):
    # 1° ≈ 111 km
    return math.hypot(c1[0]-c2[0], c1[1]-c2[1]) * 111

def consumo_gasolina(dist_km):
    return dist_km / 10

def calcular_vrp(data):
    origen = data.get("ciudad_origen")
    destino = data.get("ciudad_destino")
    max_pedidos = int(data.get("pedidos", 0))
    max_dist = float(data.get("distancia_maxima", 0))
    max_gas = float(data.get("gasolina", 0))

    if origen not in coord or destino not in coord:
        return {"error": "Ciudad no válida"}

    # Ruta simple: ida y vuelta a destino (puedes reemplazar con tu algoritmo voraz)
    d_ida = distancia(coord[origen], coord[destino])
    d_tot = d_ida * 2
    gas = consumo_gasolina(d_tot)

    if d_tot > max_dist:
        return {
            "distancia_km": round(d_tot,2),
            "gasolina_necesaria_l": round(gas,2),
            "pedidos_maximos_posibles": 0,
            "error": "Distancia máxima excedida"
        }
    if gas > max_gas:
        return {
            "distancia_km": round(d_tot,2),
            "gasolina_necesaria_l": round(gas,2),
            "pedidos_maximos_posibles": 0,
            "error": "Gasolina insuficiente"
        }

    # Si todo ok, asumimos que se pueden llevar todos los pedidos
    pedidos_posibles = min(max_pedidos, 10)  # o límite que definas

    return {
        "ruta": [origen, destino],
        "distancia_km": round(d_tot,2),
        "gasolina_necesaria_l": round(gas,2),
        "pedidos_maximos_posibles": pedidos_posibles
    }
