import sqlite3

# Función para crear la tabla de materias
def crear_tabla_materias():
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()

    # Crear la tabla "materias" si no existe
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS materias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE,
        tipo TEXT,
        semestre INTEGER
    )""")

    conn.commit()
    conn.close()

# Función para insertar las materias en la base de datos
def insertar_materias():
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()

    # Lista de materias para insertar en la base de datos
    materias = [
        ("Administración de base de datos", "SS", 6),
        ("Taller de investigación 1", "SS", 6),
        ("Ingeniería de software", "Sist ED", 6),
        ("Lenguajes de interfaz", "SS", 6),
        ("Redes de computadoras", "Sist ED", 6),
        ("Lenguajes y autómatas", "Sist ED", 6)
    ]

    # Insertar las materias en la tabla
    for materia in materias:
        cursor.execute("""
        INSERT OR IGNORE INTO materias (nombre, tipo, semestre)
        VALUES (?, ?, ?)
        """, materia)

    conn.commit()
    conn.close()

# Llamar a las funciones para crear la tabla y insertar las materias
crear_tabla_materias()
insertar_materias()

# Función para leer las palabras del archivo "archivotron.txt"
def obtener_palabras_archivotron():
    try:
        with open("archivotron.txt", "r") as file:
            palabras = file.readlines()
        return [palabra.strip() for palabra in palabras]
    except FileNotFoundError:
        return []

# Función para agregar palabras al archivo "archivotron.txt"
def agregar_palabra_archivotron(palabra):
    with open("archivotron.txt", "a") as file:
        file.write(palabra + "\n")
