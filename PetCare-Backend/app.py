import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Función auxiliar para conectarse a la base de datos
def get_db_connection():
    conn = sqlite3.connect('petcare.db')
    conn.row_factory = sqlite3.Row # Esto permite acceder a las columnas por nombre
    return conn

@app.route('/')
def home():
    return "¡Servidor PetCare con Base de Datos SQL Activo! 🗄️"

@app.route('/api/login', methods=['POST'])
def login():
    datos = request.get_json()
    usuario_recibido = datos.get('usuario')
    password_recibido = datos.get('password')

    print(f"🔍 Buscando en SQL a: {usuario_recibido}")

    # 1. Conectamos a la DB
    conn = get_db_connection()

    # 2. Ejecutamos la consulta SQL (SELECT)
    # El '?' es por seguridad (evita inyecciones SQL básicas)
    usuario_en_db = conn.execute('SELECT * FROM usuarios WHERE username = ? AND password = ?', 
                                 (usuario_recibido, password_recibido)).fetchone()

    conn.close() # Siempre cerrar la conexión

    # 3. Validamos si encontramos algo
    if usuario_en_db:
        return jsonify({
            "exito": True,
            "mensaje": f"¡Bienvenido de nuevo, {usuario_en_db['username']}!",
            "rol": usuario_en_db['rol']
        })
    else:
        return jsonify({
            "exito": False,
            "mensaje": "Usuario o contraseña incorrectos en la Base de Datos."
        }), 401

# --- NUEVA RUTA: REGISTRO ---
@app.route('/api/register', methods=['POST'])
def register():
    datos = request.get_json()
    usuario_nuevo = datos.get('usuario')
    password_nuevo = datos.get('password')
    
    # Validación simple
    if not usuario_nuevo or not password_nuevo:
        return jsonify({"exito": False, "mensaje": "Faltan datos"}), 400

    conn = get_db_connection()
    try:
        # Intentamos insertar (SQL INSERT)
        # Si el usuario ya existe, dará error porque definimos 'UNIQUE' en la base de datos
        conn.execute('INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)',
                     (usuario_nuevo, password_nuevo, 'Cliente'))
        conn.commit() # ¡Importante! Guardar cambios
        mensaje = "Usuario creado exitosamente"
        exito = True
    except sqlite3.IntegrityError:
        mensaje = "Error: El usuario ya existe."
        exito = False
    finally:
        conn.close()

    return jsonify({"exito": exito, "mensaje": mensaje})
if __name__ == '__main__':
    app.run(debug=True, port=5000)