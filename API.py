from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

FILE = "sensores.json"

# -------------------------
# CARGAR DATOS
# -------------------------
def cargar_datos():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)

def guardar_datos(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

sensores = cargar_datos()

# -------------------------
# VALIDACIONES
# -------------------------
def validar_sensor(sensor):
    tipos_validos = ["temperatura", "presion", "velocidad"]

    if sensor["type"] not in tipos_validos:
        return False, "Tipo inválido"

    valor = sensor["value"]

    if sensor["type"] == "temperatura" and not (-10 <= valor <= 100):
        return False, "Temperatura fuera de rango"

    if sensor["type"] == "presion" and not (0 <= valor <= 500):
        return False, "Presión fuera de rango"

    if sensor["type"] == "velocidad" and not (0 <= valor <= 150):
        return False, "Velocidad fuera de rango"

    return True, ""


# -------------------------
# GET TODOS
# -------------------------
@app.route("/sensors", methods=["GET"])
def get_sensors():
    return jsonify(sensores)


# -------------------------
# GET POR ID
# -------------------------
@app.route("/sensors/<int:sensor_id>", methods=["GET"])
def get_sensor(sensor_id):
    sensor = next((s for s in sensores if s["sensor_id"] == sensor_id), None)
    if not sensor:
        return jsonify({"error": "No encontrado"}), 404
    return jsonify(sensor)


# -------------------------
# POST
# -------------------------
@app.route("/sensors", methods=["POST"])
def add_sensor():
    nuevo = request.json

    if any(s["sensor_id"] == nuevo["sensor_id"] for s in sensores):
        return jsonify({"error": "ID duplicado"}), 400

    valido, msg = validar_sensor(nuevo)
    if not valido:
        return jsonify({"error": msg}), 400

    sensores.append(nuevo)
    guardar_datos(sensores)

    return jsonify(nuevo), 201


# -------------------------
# PUT
# -------------------------
@app.route("/sensors/<int:sensor_id>", methods=["PUT"])
def update_sensor(sensor_id):
    datos = request.json

    for i, s in enumerate(sensores):
        if s["sensor_id"] == sensor_id:

            valido, msg = validar_sensor(datos)
            if not valido:
                return jsonify({"error": msg}), 400

            sensores[i] = datos
            guardar_datos(sensores)
            return jsonify(datos)

    return jsonify({"error": "No encontrado"}), 404


# -------------------------
# DELETE
# -------------------------
@app.route("/sensors/<int:sensor_id>", methods=["DELETE"])
def delete_sensor(sensor_id):
    global sensores

    sensores = [s for s in sensores if s["sensor_id"] != sensor_id]
    guardar_datos(sensores)

    return jsonify({"mensaje": "Eliminado"})


# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)