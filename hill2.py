import math
import random

# Coordenadas de las ciudades
coord = {
    'Jiloyork': (19.916012, -99.580580),
    'Toluca': (19.289165, -99.655697),
    'Atlacomulco': (19.799520, -99.873844),
    'Guadalajara': (20.677754472859146, -103.34625354877137),
    'Monterrey': (25.69161110159454, -100.321838480256),
    'QuintanaRoo': (21.163111924844458, -86.80231502121464),
    'Michohacan': (19.701400113725654, -101.20829680213464),
    'Aguascalientes': (21.87641043660486, -102.26438663286967),
    'CDMX': (19.432713075976878, -99.13318344772986),
    'QRO': (20.59719437542255, -100.38667040246602)
}

# Calcular distancia euclidiana entre dos coordenadas
def distancia(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

# Calcular la distancia total de una ruta
def evalua_ruta(ruta):
    total = 0
    for i in range(len(ruta) - 1):
        ciudad1 = ruta[i]
        ciudad2 = ruta[i + 1]
        total += distancia(coord[ciudad1], coord[ciudad2])
    total += distancia(coord[ruta[-1]], coord[ruta[0]])  # volver al inicio
    return total

# Algoritmo Hill Climbing Iterativo
def i_hill_climbing():
    ciudades = list(coord.keys())
    mejor_ruta = ciudades[:]
    random.shuffle(mejor_ruta)
    mejor_distancia = evalua_ruta(mejor_ruta)
    
    max_iteraciones = 100

    while max_iteraciones > 0:
        ruta_actual = ciudades[:]
        random.shuffle(ruta_actual)
        mejora = True

        while mejora:
            mejora = False
            dist_actual = evalua_ruta(ruta_actual)
            for i in range(len(ruta_actual)):
                for j in range(i + 1, len(ruta_actual)):
                    ruta_tmp = ruta_actual[:]
                    ruta_tmp[i], ruta_tmp[j] = ruta_tmp[j], ruta_tmp[i]
                    dist_tmp = evalua_ruta(ruta_tmp)
                    if dist_tmp < dist_actual:
                        ruta_actual = ruta_tmp
                        mejora = True
                        break
                if mejora:
                    break

        dist_nueva = evalua_ruta(ruta_actual)
        if dist_nueva < mejor_distancia:
            mejor_ruta = ruta_actual
            mejor_distancia = dist_nueva
        
        max_iteraciones -= 1

    return mejor_ruta

# Punto de entrada
if __name__ == "__main__":
    ruta = i_hill_climbing()
    print("Mejor ruta encontrada:")
    print(ruta)
    print("Distancia total:", evalua_ruta(ruta))
