import sqlite3

# 1. Conectamos (o creamos) el archivo de base de datos
conn = sqlite3.connect('petcare.db')
cursor = conn.cursor()

# 2. Creamos la tabla USUARIOS (si no existe)
# Fíjate que usamos sintaxis SQL estándar
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        rol TEXT DEFAULT 'Usuario'
    )
''')

# 3. Insertamos datos de prueba (Seed Data)
# Usamos 'INSERT OR IGNORE' para no repetir si corres el script dos veces
usuarios_iniciales = [
    ('JuanPerez', 'admin123', 'Admin'),
    ('MariaSistemas', 'utp2026', 'Veterinaria'),
    ('CarlosDueño', 'perro123', 'Cliente')
]

cursor.executemany('''
    INSERT OR IGNORE INTO usuarios (username, password, rol)
    VALUES (?, ?, ?)
''', usuarios_iniciales)

# 4. Guardamos cambios y cerramos
conn.commit()
conn.close()

print("✅ Base de datos 'petcare.db' creada y usuarios iniciales insertados.")