from flask import Flask, request, jsonify, render_template
from VRP import calcular_vrp

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/api/vrp", methods=["POST"])
def api_vrp():
    data = request.get_json()
    resultado = calcular_vrp(data)
    status = 200 if 'error' not in resultado else 400
    return jsonify(resultado), status

if __name__ == "__main__":
    app.run(debug=True)
