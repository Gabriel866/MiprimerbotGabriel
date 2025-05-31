import importlib
import sqlite3
from dotenv import load_dotenv
from telegram import Update, InputFile
from telegram.ext import Application, MessageHandler, filters, CallbackContext, CommandHandler
import archivotron
import os
from telegram import ReplyKeyboardMarkup


load_dotenv() 
token_telgram = os.environ['token']

RUTA_IMAGENES = r"C:\\Users\\garoi\\OneDrive\\Desktop\\SCHOOL\\6to_SEMESTRE\\3.- LENGUAJES Y AUTOMATAS\\imagen"

def init_db():
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS materias")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS materias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE,
        tipo TEXT,
        semestre INTEGER
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ayudas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        palabra_clave TEXT UNIQUE,
        contenido TEXT
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS menus (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE,
        opciones TEXT
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS palabras_clave (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        palabra TEXT UNIQUE,
        respuesta TEXT
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS imagenes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        equipo TEXT,
        descripcion TEXT,
        ruta TEXT
    )""")
    conn.commit()
    conn.close()

def insertar_materias():
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()
    materias = [
        ("Administración de base de datos", "SS", 6),
        ("Taller de investigación 1", "SS", 6),
        ("Ingeniería de software", "Sist ED", 6),
        ("Lenguajes de interfaz", "SS", 6),
        ("Redes de computadoras", "Sist ED", 6),
        ("Lenguajes y autómatas", "Sist ED", 6)
    ]
    for materia in materias:
        cursor.execute("""
        INSERT OR IGNORE INTO materias (nombre, tipo, semestre)
        VALUES (?, ?, ?)
        """, materia)
    conn.commit()
    conn.close()

def insertar_datos_db():
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menus WHERE nombre = 'menu'")
    if not cursor.fetchone():
        cursor.execute("""
        INSERT INTO menus (nombre, opciones)
        VALUES ('menu', '1. Calificaciones, 2. Materias, 3. Maestros')
        """)
    cursor.execute("SELECT * FROM ayudas WHERE palabra_clave = 'ayuda'")
    if not cursor.fetchone():
        cursor.execute("""
        INSERT INTO ayudas (palabra_clave, contenido)
        VALUES ('ayuda', 'Este es el contenido de la ayuda.')
        """)
    cursor.execute("SELECT * FROM palabras_clave WHERE palabra = 'calificaciones'")
    if not cursor.fetchone():
        cursor.execute("""
        INSERT INTO palabras_clave (palabra, respuesta)
        VALUES ('calificaciones', 'Aquí están tus calificaciones.')
        """)
    conn.commit()
    conn.close()

def obtener_datos_db():
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT palabra_clave, contenido FROM ayudas")
    ayudas = {fila[0].lower(): fila[1] for fila in cursor.fetchall()}
    cursor.execute("SELECT nombre, opciones FROM menus")
    menus = {fila[0].lower(): fila[1] for fila in cursor.fetchall()}
    cursor.execute("SELECT palabra, respuesta FROM palabras_clave")
    palabras_clave = {fila[0].lower(): fila[1] for fila in cursor.fetchall()}
    cursor.execute("SELECT nombre, tipo, semestre FROM materias")
    materias = {fila[0].lower(): f"{fila[1]} - Semestre: {fila[2]}" for fila in cursor.fetchall()}
    conn.close()
    return ayudas, menus, palabras_clave, materias

def consultar_db(tabla):
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {tabla}")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

async def consultar(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("Uso: /consultar <nombre_tabla>")
        return
    tabla = context.args[0]
    resultados = consultar_db(tabla)
    respuesta = f"Resultados de la tabla '{tabla}':\n" if resultados else f"No se encontraron datos en la tabla '{tabla}'."
    for fila in resultados:
        respuesta += f"{fila}\n"
    await update.message.reply_text(respuesta)

##async def start(update: Update, context: CallbackContext):
   ## await update.message.reply_text("\u00a1Hola! Envíame un mensaje y verificaré las palabras.")

async def start(update: Update, context: CallbackContext):
    keyboard = [
        ["/consultar materias", "/buscarimagen"],
       ## ["materias", "calificaciones"],
      ##  ["ayuda", "menu"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "¡Hola! Usa los botones o escribe un mensaje, y te ayudaré con base en la base de datos.",
        reply_markup=reply_markup
    )


async def manejar_imagen(update: Update, context: CallbackContext):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    equipo = "equipo_default"
    descripcion = "sin_descripcion"
    if update.message.caption:
        partes = update.message.caption.split(";")
        if len(partes) == 2:
            equipo = partes[0].strip()
            descripcion = partes[1].strip()
    folder_path = os.path.join(RUTA_IMAGENES, equipo)
    os.makedirs(folder_path, exist_ok=True)
    filename = f"{descripcion.replace(' ', '_')}.jpg"
    file_path = os.path.join(folder_path, filename)
    await file.download_to_drive(file_path)
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO imagenes (equipo, descripcion, ruta)
        VALUES (?, ?, ?)
    """, (equipo, descripcion, file_path))
    conn.commit()
    conn.close()
    await update.message.reply_text(f"\u2705 Imagen guardada en '{equipo}' con descripción: '{descripcion}'.")

async def buscar_imagen(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("Uso: /buscarimagen <equipo>")
        return
    equipo = context.args[0].strip().lower()
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT descripcion, ruta FROM imagenes WHERE LOWER(equipo) = ?", (equipo,))
    resultados = cursor.fetchall()
    conn.close()
    if not resultados:
        await update.message.reply_text(f"No se encontraron imágenes para el equipo '{equipo}'.")
        return
    for descripcion, ruta in resultados:
        try:
            with open(ruta, "rb") as img:
                await update.message.reply_photo(photo=InputFile(img), caption=f"{equipo} - {descripcion}")
        except Exception as e:
            await update.message.reply_text(f"Error al abrir la imagen '{descripcion}': {e}")

async def analizar_mensaje(update: Update, context: CallbackContext):
    importlib.reload(archivotron)
    palabras_validas = archivotron.palabras_validas
    palabras_prohibidas = archivotron.palabras_prohibidas
    palabras_especiales = archivotron.palabras_especiales
    ayudas, menus, palabras_clave, materias = obtener_datos_db()
    user_text = update.message.text.lower()
    palabras = user_text.split()
    respuesta = ""
    if "materias" in palabras:
        for nombre_materia, detalle in materias.items():
            respuesta += f"\ud83d\udcda Materia: {nombre_materia.title()}, {detalle}\n"
    for palabra in palabras:
        if palabra in palabras_prohibidas:
            respuesta += f"\u26a0\ufe0f La palabra '{palabra}' está en la lista prohibida.\n"
        elif palabra in palabras_especiales:
            respuesta += f"\u2b50 La palabra '{palabra}' está en la lista especial.\n"
        elif palabra in palabras_validas:
            respuesta += f"\u2705 La palabra '{palabra}' está en la lista válida.\n"
        elif palabra in ayudas:
            respuesta += f"\ud83d\udcd6 Ayuda sobre '{palabra}': {ayudas[palabra]}\n"
        elif palabra in menus:
            respuesta += f"\ud83d\udccc Menú '{palabra}': {menus[palabra]}\n"
        elif palabra in palabras_clave:
            respuesta += f"\ud83d\udd11 '{palabra}': {palabras_clave[palabra]}\n"
        elif palabra in materias:
            respuesta += f"\ud83d\udcda Materia: '{palabra}', {materias[palabra]}\n"
    await update.message.reply_text(respuesta if respuesta else "No se encontraron coincidencias.")



init_db()
insertar_datos_db()
insertar_materias()

app = Application.builder().token(token_telgram).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("consultar", consultar))
app.add_handler(CommandHandler("buscarimagen", buscar_imagen))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analizar_mensaje))
app.add_handler(MessageHandler(filters.PHOTO, manejar_imagen))


print("🤖 Bot de filtrado iniciado...")
app.run_polling()
