from flask import Flask, request, jsonify, render_template
import math
import random

app = Flask(__name__)
ciudades = {}

def distancia(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def evalua_ruta(ruta):
    total = 0
    for i in range(len(ruta) - 1):
        total += distancia(ciudades[ruta[i]], ciudades[ruta[i+1]])
    total += distancia(ciudades[ruta[-1]], ciudades[ruta[0]])  # retorno
    return total

def i_hill_climbing():
    if len(ciudades) < 2:
        return [], 0

    lista_ciudades = list(ciudades.keys())
    mejor_ruta = lista_ciudades[:]
    random.shuffle(mejor_ruta)
    mejor_distancia = evalua_ruta(mejor_ruta)

    for _ in range(100):
        ruta_actual = lista_ciudades[:]
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

    return mejor_ruta, mejor_distancia

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agregar_ciudad', methods=['POST'])
def agregar_ciudad():
    data = request.json
    nombre = data['nombre']
    lat, lon = map(float, data['coordenadas'].split(','))
    ciudades[nombre] = (lat, lon)
    return jsonify({"mensaje": "Ciudad agregada con éxito"})

@app.route('/eliminar_ciudad', methods=['POST'])
def eliminar_ciudad():
    nombre = request.json['nombre']
    if nombre in ciudades:
        del ciudades[nombre]
        return jsonify({"mensaje": "Ciudad eliminada"})
    return jsonify({"mensaje": "Ciudad no encontrada"}), 404

@app.route('/editar_ciudad', methods=['POST'])
def editar_ciudad():
    data = request.json
    nombre = data['nombre']
    lat, lon = map(float, data['coordenadas'].split(','))
    if nombre in ciudades:
        ciudades[nombre] = (lat, lon)
        return jsonify({"mensaje": "Ciudad editada con éxito"})
    return jsonify({"mensaje": "Ciudad no encontrada"}), 404

@app.route('/calcular_ruta', methods=['POST'])
def calcular_ruta():
    global ciudades
    data = request.get_json()
    ciudades = {ciudad["nombre"]: (ciudad["lat"], ciudad["lon"]) for ciudad in data["ciudades"]}
    ruta, distancia_total = i_hill_climbing()
    return jsonify({
        "ruta": ruta,
        "distancia": round(distancia_total, 2)
    })


if __name__ == '__main__':
    app.run(debug=True)
