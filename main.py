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
    descuento = p["discountPercentage"]
    rating = p["rating"]
    categoria = p["category"]

    precio_venta = precio * 1.4
    ganancia = precio_venta - precio
    margen = (ganancia / precio) * 100

    if (
        descuento > 10 and
        rating >= 4.0 and
        precio < 100 and
        ganancia > 5 and
        margen > 25
    ):
        precio_base = precio / (1 - descuento / 100)

demanda_score = rating * 20

indice_compra = (
    margen * 0.4 +
    descuento * 0.3 +
    (rating * 10) * 0.3
)

if indice_compra > 35:
    decision = "COMPRAR"
else:
    decision = "IGNORAR"

candidatos.append([
    titulo,
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
candidatos.sort(key=lambda x: x[8], reverse=True)

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
    ["Filtro activo:", "descuento>10, rating>=4, precio<100, ganancia>5, margen>25"],
    [""]
]

live_sheet.update("A1", resumen + encabezados + candidatos)

#------- HISTORICO -------
historico_data = historico_sheet.get_all_values()

if not historico_data or historico_data[0][0] != "timestamp":
    historico_sheet.clear()
    historico_sheet.append_row([
        "timestamp",
        "producto",
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
    ])

filas_historico = [[ahora] + fila for fila in candidatos]

# limpiar registros con más de 30 días
historico_data = historico_sheet.get_all_values()

if historico_data:
    encabezado_historico = historico_data[0]
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
    historico_sheet.update("A1", [encabezado_historico] + filas_validas)

print("Datos enviados a Google Sheets")
print("Total:", len(candidatos)) 