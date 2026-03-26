import json
import os
import requests
import gspread
from datetime import datetime, timedelta
from google.oauth2.service_account import Credentials

# -----------------------------
# 1. Obtener productos
# -----------------------------
def obtener_productos():
    url = "https://dummyjson.com/products"
    response = requests.get(url)
    data = response.json()
    return data["products"]

def filtrar_productos(productos):
    candidatos = []
    for p in productos:
        titulo = p["title"]
        precio = p["price"]
        categoria = p["category"].lower()
        descuento = p["discountPercentage"]
        rating = p["rating"]

        # Filtrar por categoría
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

        # Evaluar decisión
        decision = evaluar_decision(margen, rating, precio, descuento)

        if decision == "❌ DESCARTAR":
            continue

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
    return candidatos

def evaluar_decision(margen, rating, precio, descuento):
    if (
        margen >= 25 and
        rating >= 4.0 and
        precio <= 200 and
        descuento >= 5
    ):
        return "🔥 OPORTUNIDAD"
    elif (
        margen >= 18 and
        rating >= 3.8 and
        precio <= 250
    ):
        return "⚠️ MEDIA"
    else:
        return "❌ DESCARTAR"

# -----------------------------
# 2. Conectar a Google Sheets
# -----------------------------
def conectar_google_sheets():
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
    return gspread.authorize(creds)

def obtener_hojas(spreadsheet):
    try:
        live_sheet = spreadsheet.worksheet("LIVE")
    except:
        live_sheet = spreadsheet.add_worksheet(title="LIVE", rows="100", cols="20")

    try:
        historico_sheet = spreadsheet.worksheet("HISTORICO")
    except:
        historico_sheet = spreadsheet.add_worksheet(title="HISTORICO", rows="1000", cols="20")

    return live_sheet, historico_sheet

# -----------------------------
# 3. Subir datos
# -----------------------------
def subir_datos(live_sheet, historico_sheet, candidatos):
    live_sheet.clear()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

    resumen = [
        ["Última ejecución:", ahora],
        ["Fuente:", "dummyjson"],
        ["Total candidatos:", len(candidatos)],
        ["Filtro activo:", "margen>=25, rating>=4.0, precio<=200, descuento>=5, solo smartphones/laptops"],
        [""]
    ]

    live_sheet.update("A1", resumen + encabezados + candidatos)

    # Manejo de histórico
    manejar_historico(historico_sheet, candidatos, ahora)

def manejar_historico(historico_sheet, candidatos, ahora):
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

    # Validar encabezado
    if not historico_data or historico_data[0] != encabezado_historico[0]:
        historico_sheet.clear()
        historico_sheet.update("A1", encabezado_historico)
        historico_data = historico_sheet.get_all_values()

    # Insertar nuevos datos
    filas_historico = [[ahora] + fila for fila in candidatos]
    if filas_historico:
        historico_sheet.insert_rows(filas_historico, row=2)

    # Limpiar registros con más de 30 días
    limpiar_historico(historico_sheet, historico_data)

def limpiar_historico(historico_sheet, historico_data, encabezado_historico):
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
        historico_sheet.update("A1",encabezado_historico + filas_validas)

# -----------------------------
# Ejecución del script
# -----------------------------
if __name__ == "__main__":
    productos = obtener_productos()
    candidatos = filtrar_productos(productos)
    candidatos.sort(key=lambda x: x[10], reverse=True)

    client = conectar_google_sheets()
    spreadsheet = client.open("Arbitraje IA Demo")
    live_sheet, historico_sheet = obtener_hojas(spreadsheet)

    subir_datos(live_sheet, historico_sheet, candidatos)

    print("Datos enviados a Google Sheets")
    print("Total:", len(candidatos))