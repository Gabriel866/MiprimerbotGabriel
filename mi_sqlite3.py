# materia.py

import sqlite3

# Función para crear la tabla de materias si no existe
def crear_tabla_materias():
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS materias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE
    )
    """)
    
    conn.commit()
    conn.close()

# Función para insertar materias en la base de datos
def insertar_materias():
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()

    materias = [
        'Administración de base de datos 6 SS',
        'Taller de investigación 1 6 SS',
        'Ingeniería de software Sist ED 6 SS',
        'Lenguajes de interfaz 6 SS',
        'Redes de computadoras Sist ED 6 SS',
        'Lenguajes y autómatas 2 Sist ED 6 SS'
    ]
    
    for materia in materias:
        cursor.execute("INSERT OR IGNORE INTO materias (nombre) VALUES (?)", (materia,))
    
    conn.commit()
    conn.close()

# Función para obtener todas las materias de la base de datos
def obtener_materias():
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT nombre FROM materias")
    materias = [fila[0] for fila in cursor.fetchall()]
    
    conn.close()
    return materias
