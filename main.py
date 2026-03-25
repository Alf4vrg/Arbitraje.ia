import requests
import gspread
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

creds = Credentials.from_service_account_file(
    "credenciales.json",
    scopes=SCOPES
)

client = gspread.authorize(creds)

# ⚠️ CAMBIA ESTE NOMBRE EXACTO
sheet = client.open("Arbitraje IA Demo").sheet1

# -----------------------------
# 3. Subir datos
# -----------------------------
sheet.clear()

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

sheet.update("A1", encabezados + candidatos)

print("Datos enviados a Google Sheets")
print("Total:", len(candidatos)) 
