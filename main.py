import json
import os
import requests
import gspread
from datetime import datetime, timedelta
from google.oauth2.service_account import Credentials

# -----------------------------
# 1. Obtener productos
# -----------------------------
url = "https://dummyjson.com/products"

response = requests.get(url)
data = response.json()

productos = data["products"]

candidatos = []

for p in productos:
    titulo = p["title"]
    precio = p["price"]
    categoria = p["category"]
    descuento = p["discountPercentage"]
    rating = p["rating"]

    # filtro de categoría
    categoria = p["category"].lower()
    if categoria not in ["smartphones", "laptops"]:
        continue

    precio_venta = precio * 1.4
    ganancia = precio_venta - precio
    margen = (ganancia / precio) * 100
    precio_base = precio / (1 - descuento / 100)

    demanda_score = rating * 20

    indice_compra = (
        margen * 0.4 +
        descuento * 0.3 +
        (rating * 10) * 0.3
    )

    if (
        margen >= 25 and
        rating >= 4.0 and
        precio <= 200 and
        descuento >= 5
    ):
        decision = "🔥 OPORTUNIDAD"
    elif margen >= 15:
        decision = "⚠️ MEDIA"
    else:
        decision = "❌ DESCARTAR"

    candidatos.append([
        titulo,
        categoria,
        round(precio, 2),
        round(precio_base, 2),
        round(precio_venta, 2),
        round(ganancia, 2),
        round(margen, 2),
        round(descuento, 2),
        round(rating, 2),
        round(demanda_score, 2),
        round(indice_compra, 2),
        decision
    ])

# ordenar por índice
candidatos.sort(key=lambda x: x[10], reverse=True)

# -----------------------------
# 2. Conectar a Google Sheets
# -----------------------------
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credenciales_json = os.getenv("GOOGLE_CREDENTIALS")

if not credenciales_json:
    raise ValueError("No se encontró la variable GOOGLE_CREDENTIALS")

credenciales_dict = json.loads(credenciales_json)

creds = Credentials.from_service_account_info(
    credenciales_dict,
    scopes=SCOPES
)


client = gspread.authorize(creds)

# ⚠️ CAMBIA ESTE NOMBRE EXACTO
spreadsheet = client.open("Arbitraje IA Demo")

# hoja LIVE
try:
    live_sheet = spreadsheet.worksheet("LIVE")
except:
    live_sheet = spreadsheet.add_worksheet(title="LIVE", rows="100", cols="20")

# hoja HISTORICO
try:
    historico_sheet = spreadsheet.worksheet("HISTORICO")
except:
    historico_sheet = spreadsheet.add_worksheet(title="HISTORICO", rows="1000", cols="20")

# -----------------------------
# 3. Subir datos
# -----------------------------
live_sheet.clear()

encabezados = [[
    "producto",
    "categoria",
    "precio_compra",
    "precio_base",
    "precio_venta",
    "ganancia",
    "margen",
    "descuento",
    "rating",
    "demanda_score",
    "indice_compra",
    "decision"
]]

ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

resumen = [
    ["Última ejecución:", ahora],
    ["Fuente:", "dummyjson"],
    ["Total candidatos:", len(candidatos)],
    ["Filtro activo:", "margen>=30, rating>=4.3, precio<=150, descuento>=10, solo electronica"],
    [""]
]

live_sheet.update("A1", resumen + encabezados + candidatos)

#------- HISTORICO -------

encabezado_historico = [[
    "timestamp",
    "producto",
    "categoria",
    "precio_compra",
    "precio_base",
    "precio_venta",
    "ganancia",
    "margen",
    "descuento",
    "rating",
    "demanda_score",
    "indice_compra",
    "decision"
]]

historico_data = historico_sheet.get_all_values()

# validar encabezado
if not historico_data or historico_data[0] != encabezado_historico[0]:
    historico_sheet.clear()
    historico_sheet.update("A1", encabezado_historico)
    historico_data = historico_sheet.get_all_values()

# insertar nuevos datos debajo del encabezado
filas_historico = [[ahora] + fila for fila in candidatos]

if filas_historico:
    historico_sheet.insert_rows(filas_historico, row=2)

# limpiar registros con más de 30 días
historico_data = historico_sheet.get_all_values()

if len(historico_data) > 1:
    filas_validas = []
    limite = datetime.now() - timedelta(days=30)

    for fila in historico_data[1:]:
        if not fila or not fila[0].strip():
            continue

        try:
            fecha_fila = datetime.strptime(fila[0], "%Y-%m-%d %H:%M:%S")
            if fecha_fila >= limite:
                filas_validas.append(fila)
        except:
            continue

    historico_sheet.clear()
    historico_sheet.update("A1", encabezado_historico + filas_validas)

print("Datos enviados a Google Sheets")
print("Total:", len(candidatos)) 