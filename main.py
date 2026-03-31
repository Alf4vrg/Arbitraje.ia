# import json
# import os
# import requests
# import gspread
# from datetime import datetime, timedelta
# from google.oauth2.service_account import Credentials

# # -----------------------------
# # 1. Obtener productos
# # -----------------------------
# def obtener_aliexpress():
#     url = "https://dummyjson.com/products/category/smartphones"
#     response = requests.get(url)
#     data = response.json()

#     print("STATUS:", response.status_code)
#     print("RESPUESTA:", data.keys())

#     return data.get("products", [])

# def filtrar_productos(productos):
#     candidatos = []
#     print(sorted(set(p["category"] for p in productos)))
#     for p in productos:
#         titulo = p["title"]
#         precio = p["price"]
#         categoria = p["category"].lower()
#         descuento = p["discountPercentage"]
#         rating = p["rating"]
#         demanda_score = rating * 20

#         # Filtrar por categoría
#         categorias_validas = [
#             "smartphones",
#             "laptops",
#             "mobile-accessories",
#             "tablets"
#         ]

#         if categoria not in categorias_validas:
#             continue

#         tipo_cambio = 17  # MXN por USD

#         precio_compra = precio * tipo_cambio
#         precio_base = (precio / (1 - descuento / 100)) * tipo_cambio
#         precio_venta = precio_compra * 1.8
#         ganancia = precio_venta - precio_compra
#         margen = (ganancia / precio_compra) * 100
#         demanda_score = rating * 20

#         if margen < 30:
#             continue

#         indice_compra = (
#             margen * 0.4 +
#             descuento * 0.3 +
#             (rating * 10) * 0.3
#         )

#         # Evaluar decisión
#         decision = evaluar_decision(margen, rating, precio_compra, descuento)

#         if decision == "❌ DESCARTAR":
#             continue

#         if decision == "🔥 OPORTUNIDAD":
#             print(f"{titulo}")
#             print(f"Compra: ${round(precio_compra, 2)} MXN")
#             print(f"Venta: ${round(precio_venta, 2)} MXN")
#             print(f"Ganancia: ${round(ganancia, 2)} MXN ({round(margen, 2)}%)")
#             print(f"Rating: {round(rating, 2)}")
#             print(f"Descuento: {round(descuento, 2)}%")
#             print("🔥 OPORTUNIDAD")
#             print("------")


#             candidatos.append([
#             titulo,
#             categoria,
#             round(precio_compra, 2),
#             round(precio_base, 2),
#             round(precio_venta, 2),
#             round(ganancia, 2),
#             round(margen, 2),
#             round(descuento, 2),
#             round(rating, 2),
#             round(demanda_score, 2),
#             round(indice_compra, 2),
#             decision,
            
#         ])
#     return candidatos

# def evaluar_decision(margen, rating, precio, descuento):
#     if (
#         margen >= 35 and
#         rating >= 4.4 and
#         precio <= 12000 and
#         descuento >= 8
#     ):
#         return "🔥 OPORTUNIDAD"
#     elif (
#         margen >= 20 and
#         rating >= 4.0 and
#         precio <= 18000
#     ):
#         return "⚠️ MEDIA"
#     else:
#         return "❌ DESCARTAR"
    
# def calcular_ganancia_real(precio_compra, precio_venta_real):
#     if not precio_venta_real or precio_venta_real <= 0:
#         return 0
#     return round(precio_venta_real - precio_compra, 2)

# def calcular_margen_real(precio_compra, precio_venta_real):
#     if not precio_venta_real or precio_venta_real <= 0:
#         return 0
#     return round((precio_venta_real - precio_compra) / precio_compra * 100, 2)

# def clasificar_validacion(margen_estimado, margen_real, precio_venta_real):
#     if not precio_venta_real or precio_venta_real <= 0 or margen_real <= 0:
#         return "❓ SIN VALIDAR"

#     if margen_real >= 20:
#         return "✅ REAL"

#     if margen_real < 20 and margen_estimado >= 40:
#         return "⚠️ INFLADO"

#     return "⚠️ INFLADO"

# def decidir_compra_final(margen_real, demanda_score):
#     if margen_real >= 30 and demanda_score >= 85:
#         return "🔥 COMPRAR"
#     elif margen_real >= 20 and demanda_score >= 75:
#         return "⚠️ REVISAR"
#     else:
#         return "❌ DESCARTAR"

# def asignar_capital(decision_final, margen_real, demanda_score, capital_total, total_comprar, total_revisar):
#     capital_invertible = capital_total * 0.75

#     if decision_final == "🔥 COMPRAR" and total_comprar > 0:
#         return round((capital_invertible * 0.35) / total_comprar, 2)

#     elif decision_final == "⚠️ REVISAR" and total_revisar > 0:
#         return round((capital_invertible * 0.40) / total_revisar, 2)

#     else:
#         return 0
    
# def limpiar_numero(valor):
#     if valor is None:
#         return 0.0

#     texto = str(valor).strip()

#     if not texto:
#         return 0.0

#     texto = texto.replace("$", "").replace("MXN", "").replace(" ", "")

#     # Si viene con coma decimal tipo 5949,83
#     if "," in texto and "." not in texto:
#         texto = texto.replace(",", ".")

#     # Si viene con comas de miles tipo 10,699.50
#     elif "," in texto and "." in texto:
#         texto = texto.replace(",", "")

#     return float(texto)

# def recalcular_ganancia_real_en_sheet(live_sheet):
#     datos = live_sheet.get_all_values()

#     if len(datos) < 7:
#         return

#     encabezados = datos[5]  # fila 6

#     idx_precio_compra = encabezados.index("precio_compra")
#     idx_precio_venta_real = encabezados.index("precio_venta_real")
#     idx_ganancia_real = encabezados.index("ganancia_real")
#     idx_margen_real = encabezados.index("margen_real")
#     idx_estado_validacion = encabezados.index("estado_validacion")
#     idx_margen_estimado = encabezados.index("margen")
#     idx_demanda_score = encabezados.index("demanda_score")
#     idx_decision_final = encabezados.index("decision_final")
#     idx_capital_sugerido = encabezados.index("capital_sugerido")
#     total_comprar = sum(1 for fila in datos if "🔥 COMPRAR" in fila)
#     total_revisar = sum(1 for fila in datos if "⚠️ REVISAR" in fila)
#     capital_total = 9000

#     for i in range(6, len(datos)):  # desde fila 7
#         fila = datos[i]

#         try:
#             precio_compra = limpiar_numero(fila[idx_precio_compra]) if idx_precio_compra < len(fila) else 0
#             precio_venta_real = limpiar_numero(fila[idx_precio_venta_real]) if idx_precio_venta_real < len(fila) else 0
#             ganancia_real = calcular_ganancia_real(precio_compra, precio_venta_real)
#             margen_real = calcular_margen_real(precio_compra, precio_venta_real)
#             margen_estimado = limpiar_numero(fila[idx_margen_estimado]) if idx_margen_estimado < len(fila) else 0
#             estado_validacion = clasificar_validacion(margen_estimado, margen_real, precio_venta_real)
#             demanda_score = limpiar_numero(fila[idx_demanda_score]) if idx_demanda_score < len(fila) else 0
#             decision_final = decidir_compra_final(margen_real, demanda_score)
#             capital_sugerido = asignar_capital(
#                 decision_final,
#                 margen_real,
#                 demanda_score,
#                 capital_total,
#                 total_comprar,
#                 total_revisar
#         )
        
#             live_sheet.update_cell(i + 1, idx_ganancia_real + 1, ganancia_real)
#             live_sheet.update_cell(i + 1, idx_margen_real + 1, margen_real)
#             live_sheet.update_cell(i + 1, idx_estado_validacion + 1, estado_validacion)
#             live_sheet.update_cell(i + 1, idx_decision_final + 1, decision_final)
#             live_sheet.update_cell(i + 1, idx_capital_sugerido + 1, capital_sugerido)
#         except Exception as e:
#             print(f"Error en fila {i+1}: {e}")
#             continue
#                                                                                                                                         # -----------------------------# -----------------------------# -----------------------------
# # 2. Conectar a Google Sheets
# # -----------------------------
# def conectar_google_sheets():
#     SCOPES = [
#         "https://www.googleapis.com/auth/spreadsheets",
#         "https://www.googleapis.com/auth/drive"
#     ]

#     credenciales_json = os.getenv("GOOGLE_CREDENTIALS")
#     if not credenciales_json:
#         raise ValueError("No se encontró la variable GOOGLE_CREDENTIALS")

#     credenciales_dict = json.loads(credenciales_json)
#     creds = Credentials.from_service_account_info(
#         credenciales_dict,
#         scopes=SCOPES
#     )
#     return gspread.authorize(creds)

# def obtener_hojas(spreadsheet):
#     try:
#         live_sheet = spreadsheet.worksheet("LIVE")
#     except:
#         live_sheet = spreadsheet.add_worksheet(title="LIVE", rows="100", cols="20")

#     try:
#         historico_sheet = spreadsheet.worksheet("HISTORICO")
#     except:
#         historico_sheet = spreadsheet.add_worksheet(title="HISTORICO", rows="1000", cols="20")

#     return live_sheet, historico_sheet

# # -----------------------------
# # 3. Subir datos
# # -----------------------------
# def subir_datos(live_sheet, historico_sheet, candidatos):
#     #live_sheet.clear()
#     ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     encabezados = [[
#         "producto",
#         "categoria",
#         "precio_compra",
#         "precio_base",
#         "precio_venta",
#         "ganancia",
#         "margen",
#         "descuento",
#         "rating",
#         "demanda_score",
#         "indice_compra",
#         "decision",
#     ]]

#     resumen = [
#         ["Última ejecución:", ahora],
#         ["Fuente:", "dummyjson"],
#         ["Total candidatos:", len(candidatos)],
#         ["Filtro activo:", "margen>=20, rating>=4.0, precio<=250, descuento>=5, solo beauty/fragrances"],
#         [""]
#     ]

#     live_sheet.update("A1", resumen + encabezados + candidatos)

#     recalcular_ganancia_real_en_sheet(live_sheet)
#     # Manejo de histórico
#     manejar_historico(historico_sheet, candidatos, ahora)

# def manejar_historico(historico_sheet, candidatos, ahora):
#     encabezado_historico = [[
#         "timestamp",
#         "producto",
#         "categoria",
#         "precio_compra",
#         "precio_base",
#         "precio_venta",
#         "ganancia",
#         "margen",
#         "descuento",
#         "rating",
#         "demanda_score",
#         "indice_compra",
#         "decision"
#     ]]

#     historico_data = historico_sheet.get_all_values()

#     # Validar encabezado
#     if not historico_data or historico_data[0] != encabezado_historico[0]:
#         historico_sheet.clear()
#         historico_sheet.update("A1", encabezado_historico)
#         historico_data = historico_sheet.get_all_values()

#     # Insertar nuevos datos
#     filas_historico = [[ahora] + fila for fila in candidatos]
#     if filas_historico:
#         historico_sheet.insert_rows(filas_historico, row=2)

#     # Limpiar registros con más de 30 días
#     limpiar_historico(historico_sheet, historico_data, encabezado_historico)

# def limpiar_historico(historico_sheet, historico_data, encabezado_historico):
#     if len(historico_data) > 1:
#         filas_validas = []
#         limite = datetime.now() - timedelta(days=30)

#         for fila in historico_data[1:]:
#             if not fila or not fila[0].strip():
#                 continue
#             try:
#                 fecha_fila = datetime.strptime(fila[0], "%Y-%m-%d %H:%M:%S")
#                 if fecha_fila >= limite:
#                     filas_validas.append(fila)
#             except:
#                 continue

#         historico_sheet.clear()
#         historico_sheet.update("A1",encabezado_historico + filas_validas)

# # -----------------------------
# # Ejecución del script
# # -----------------------------
# if __name__ == "__main__":
#     productos = obtener_aliexpress()
#     candidatos = filtrar_productos(productos)
#     candidatos.sort(key=lambda x: x[10], reverse=True)

#     client = conectar_google_sheets()
#     spreadsheet = client.open("Arbitraje IA Demo")
#     live_sheet, historico_sheet = obtener_hojas(spreadsheet)

#     subir_datos(live_sheet, historico_sheet, candidatos)

#     print("Datos enviados a Google Sheets")
#     print("Total:", len(candidatos))


#if __name__ == "__main__":
#   productos_ali = obtener_aliexpress()
#
#    for p in productos_ali[:10]:
#       titulo = p["title"]
#       precio = p["price"]
#        imagen = p["thumbnail"]
#
#       print(f"{titulo} | ${precio}")
# 
#       print(imagen)
#        print("------") 

#if __name__ == "__main__":
#   productos = obtener_aliexpress()
#   candidatos = filtrar_productos(productos)
#    print("TOTAL CANDIDATOS:", len(

from app.runner import run_pipeline

if __name__ == "__main__":
    keyword = "audifonos"
    source_name = "aliexpress"

    candidates = run_pipeline(keyword, source_name)

    print(f"Candidatos: {len(candidates)}")
    for product in candidates[:5]:
        print(product.title, product.estimated_margin, product.buy_index)