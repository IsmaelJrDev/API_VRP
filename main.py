from flask import Flask, request, render_template
from VRP import vrp_voraz, coord, distancia_ruta, peso_ruta, volumen_ruta, consumo_gasolina

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    ciudades = list(coord.keys())
    rutas_info = None
    error = None

    if request.method == 'POST':
        try:
            ciudad_origen = request.form['ciudad_origen']
            ciudad_destino = request.form['ciudad_destino']
            max_carga = int(request.form['max_carga'])
            max_distancia = float(request.form['max_distancia'])
            max_gasolina = float(request.form['max_gasolina'])
            max_volumen = float(request.form['max_volumen'])

            rutas = vrp_voraz(ciudad_origen, ciudad_destino, max_carga, max_distancia, max_gasolina, max_volumen)
            rutas_info = []
            for ruta in rutas:
                dist = distancia_ruta(ruta, coord[ciudad_origen])
                rutas_info.append({
                    "ruta": ruta,
                    "peso_total": peso_ruta(ruta),
                    "distancia_total": round(dist, 2),
                    "gasolina_total": round(consumo_gasolina(dist), 2),
                    "volumen_total": volumen_ruta(ruta)
                })
        except Exception as e:
            error = str(e)

    return render_template('index.html', ciudades=ciudades, rutas_info=rutas_info, error=error)

if __name__ == '__main__':
    app.run(debug=True)
