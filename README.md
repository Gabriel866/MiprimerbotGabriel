# telegram_bot
Este bot de Telegram fue desarrollado con el objetivo de facilitar la consulta de materias, menús, ayudas y palabras clave.
así como el almacenamiento y búsqueda de imágenes clasificadas por equipos. 
Utiliza una base de datos SQLite local y permite analizar mensajes de texto con listas personalizadas.
Donde su funcion principal es la busqueda de imagenes.

## Funcionalidades
- Búsqueda de imágenes por equipo usando `/buscarimagen <equipo>`.
- Consulta de materias por texto.
- Comando `/consultar <tabla>` para inspeccionar cualquier tabla de la base de datos.
- Comando `/start` para iniciar el bot y mostrar mensaje de bienvenida.
- Almacenamiento de imágenes por equipos con descripción (a partir de fotos enviadas).
- Análisis semántico del mensaje para detectar:
- Palabras prohibidas, válidas y especiales.
- Palabras clave con respuesta.
- Palabras asociadas a ayudas o menús.
- Materias disponibles.

  ## Estructura de la Base de Datos

La base de datos `bot_data.db` contiene las siguientes tablas:

- materias(nombre, tipo, semestre)
- ayudas(palabra_clave, contenido)
- menus(nombre, opciones)
- palabras_clave(palabra, respuesta)
- imagenes(equipo, descripcion, ruta)


## Requisitos

- Python 3.10 o superior
- Telegram Bot Token
- Librerías:
  * python-telegram-bot
  * python-dotenv

## Instalación
1.- Clona el repositorio o descarga el script.
2.- Crea un archivo .env en la misma carpeta y agrega:

token=TU_TOKEN_DE_TELEGRAM

3.- Asegúrate de tener una carpeta de imágenes accesible:

C:\Users\garoi\OneDrive\Desktop\SCHOOL\6to_SEMESTRE\3.- LENGUAJES Y AUTOMATAS\imagen

4.- Ejecuta el script principal:
python bot.py

## Envío de imagenes
Para guardar una imagen, envíala al bot con un pie de foto en el siguiente formato:

<nombre_equipo> ; <descripcion>

## Consulta de imagenes

/buscarimagen <equipo>

## Comandos principales

| Comando                  | Descripción                                      |
| ------------------------ | ------------------------------------------------ |
| /start                   | Inicia el bot y muestra un mensaje de bienvenida |
| /consultar <tabla>       | Devuelve todos los registros de una tabla        |
| /buscarimagen <equipo>   | Muestra imágenes guardadas por nombre de equipo  |


## Archivos requeridos
bot.py (el archivo principal)

archivotron.py (debe contener las listas palabras_validas, palabras_prohibidas, palabras_especiales)

.env con la variable de entorno token

## Notas

* El bot recarga dinámicamente las listas desde archivotron.py cada vez que recibe un mensaje.
* Si no encuentra coincidencias, responde con un mensaje genérico.

## Licencias  
Este proyecto es de uso académico. Puedes modificarlo y adaptarlo libremente para fines educativos.

