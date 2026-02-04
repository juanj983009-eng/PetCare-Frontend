import os
import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Función para conectarse a la Base de Datos
# Ahora es inteligente: Si hay URL en la nube, la usa. Si no, usa tu archivo local.
def get_db_connection():
    db_url = os.environ.get('DATABASE_URL')

    if db_url:
        # Estamos en la NUBE (Render) -> Usamos PostgreSQL
        conn = psycopg2.connect(db_url)
    else:
        # Estamos en CASA (Local) -> Usamos SQLite
        import sqlite3
        conn = sqlite3.connect('petcare.db')
        conn.row_factory = sqlite3.Row

    return conn

# Función para inicializar la tabla (Migración automática)
# Esto creará la tabla en PostgreSQL la primera vez que arranque
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    # Crear tabla si no existe
    # Nota: Postgres y SQLite tienen sintaxis parecida para CREATE TABLE
    cur.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY, -- SERIAL es el autoincrement de Postgres
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            rol TEXT DEFAULT 'Usuario'
        );
    ''')

    # Insertar usuario Admin por defecto si está vacía
    # Usamos sintaxis compatible (ON CONFLICT para Postgres / OR IGNORE para SQLite es más complejo, 
    # así que haremos un try/except simple en Python para no complicar el SQL)
    try:
        cur.execute("INSERT INTO usuarios (username, password, rol) VALUES ('JuanAdmin', 'admin123', 'Admin')")
        conn.commit()
    except:
        pass # Si ya existe, no hacemos nada

    conn.commit()
    cur.close()
    conn.close()

# Ejecutamos la creación de tablas al iniciar
try:
    init_db()
    print("✅ Base de datos inicializada correctamente")
except Exception as e:
    print(f"⚠️ Error inicializando DB: {e}")

@app.route('/')
def home():
    return "¡Backend PetCare con PostgreSQL! 🐘"

@app.route('/api/login', methods=['POST'])
def login():
    datos = request.get_json()
    usuario = datos.get('usuario')
    password = datos.get('password')

    conn = get_db_connection()
    cur = conn.cursor()

    # IMPORTANTE: Postgres usa %s para variables, SQLite usa ?
    # Hacemos un pequeño truco para soportar ambos o forzamos %s si estamos con librería psycopg2
    try:
        # Intento sintaxis Postgres
        cur.execute('SELECT * FROM usuarios WHERE username = %s AND password = %s', (usuario, password))
    except TypeError:
        # Si falla, es porque estamos en SQLite local
        cur = conn.cursor() # Reiniciamos cursor
        cur.execute('SELECT * FROM usuarios WHERE username = ? AND password = ?', (usuario, password))

    # En psycopg2, fetchone devuelve una tupla, no un diccionario directo a menos que usemos extras.
    # Vamos a acceder por índice para ser compatibles con ambos drivers fácilmente.
    # 0=id, 1=username, 2=password, 3=rol
    user = cur.fetchone()

    cur.close()
    conn.close()

    if user:
        # Adaptamos la respuesta según lo que devolvió la DB
        # Si es sqlite con row_factory devuelve objeto, si es postgres tupla
        rol = user[3] if isinstance(user, tuple) else user['rol']
        nombre = user[1] if isinstance(user, tuple) else user['username']

        return jsonify({
            "exito": True,
            "mensaje": f"¡Bienvenido, {nombre}!",
            "rol": rol
        })
    else:
        return jsonify({"exito": False, "mensaje": "Credenciales incorrectas"}), 401

@app.route('/api/register', methods=['POST'])
def register():
    datos = request.get_json()
    usuario = datos.get('usuario')
    password = datos.get('password')

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Intentamos insertar (Sintaxis Postgres %s)
        try:
            cur.execute('INSERT INTO usuarios (username, password, rol) VALUES (%s, %s, %s)', 
                       (usuario, password, 'Cliente'))
        except TypeError:
            # Fallback para SQLite local
            cur.execute('INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)', 
                       (usuario, password, 'Cliente'))

        conn.commit()
        exito = True
        mensaje = "Usuario registrado en Nube"
    except Exception as e:
        conn.rollback() # Deshacer si hubo error
        exito = False
        mensaje = "Error: El usuario ya existe o hubo un fallo."
        print(e)
    finally:
        cur.close()
        conn.close()

    return jsonify({"exito": exito, "mensaje": mensaje})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)