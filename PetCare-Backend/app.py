from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
# Permitimos que cualquier origen (tu frontend) se conecte a este backend
CORS(app) 

# --- BASE DE DATOS SIMULADA (MOCK) ---
# Como aún no conectamos SQL, usaremos esto para probar la lógica.
USUARIOS_REGISTRADOS = {
    "JuanPerez": "admin123",
    "MariaSistemas": "utp2026"
}

@app.route('/')
def home():
    return "¡Servidor PetCare Activo! 🚀"

# --- NUEVA RUTA: LOGIN ---
# Acepta solo método POST (envío de datos)
@app.route('/api/login', methods=['POST'])
def login():
    # 1. Recibimos los datos que envía el Frontend (JSON)
    datos = request.get_json()
    usuario_recibido = datos.get('usuario')
    password_recibido = datos.get('password')

    # 2. Imprimimos en la consola de Python para ver qué llega (útil para ti)
    print(f"Intento de login: {usuario_recibido} | Pass: {password_recibido}")

    # 3. Validamos la lógica (El IF del Backend)
    # Verificamos si el usuario existe y si la contraseña coincide
    if usuario_recibido in USUARIOS_REGISTRADOS and USUARIOS_REGISTRADOS[usuario_recibido] == password_recibido:
        return jsonify({
            "exito": True,
            "mensaje": f"¡Bienvenido al sistema, {usuario_recibido}!",
            "rol": "Admin"
        })
    else:
        return jsonify({
            "exito": False,
            "mensaje": "Usuario o contraseña incorrectos."
        }), 401 # 401 es el código de error para "No autorizado"

if __name__ == '__main__':
    app.run(debug=True, port=5000)