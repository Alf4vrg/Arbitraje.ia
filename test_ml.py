from sources.mercadolibre import search_mercadolibre_prices

query = "sensor nissan"
result = search_mercadolibre_prices_playwright(query)

print("QUERY:", query)
print("RESULT:", result)