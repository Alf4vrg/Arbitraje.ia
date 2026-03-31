from sources.mercadolibre import search_mercadolibre_prices

queries = [
    "probador de relé automotriz 12v",
    "sensor de posicion del cigüeñal nissan",
    "audifonos kz edx pro",
]

for q in queries:
    result = search_mercadolibre_prices(q)
    print("\n======================")
    print("QUERY:", q)
    print("RESULT:", result)