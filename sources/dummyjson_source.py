import requests
from typing import List

from core.models import Product
from sources.base import ProductSource


class DummyJsonSource(ProductSource):
    def __init__(self) -> None:
        self.url = "https://dummyjson.com/products/category/smartphones"

    def fetch_products(self, query: str = "") -> List[Product]:
        response = requests.get(self.url, timeout=20)
        response.raise_for_status()
        data = response.json()

        products: List[Product] = []

        for item in data.get("products", []):
            products.append(
                Product(
                    source="dummyjson",
                    title=item.get("title", ""),
                    category=item.get("category", ""),
                    price=float(item.get("price", 0)),
                    currency="USD",
                    rating=float(item.get("rating", 0)),
                    discount_percent=float(item.get("discountPercentage", 0)),
                    image_url=item.get("thumbnail", ""),
                    product_url=item.get("thumbnail", ""),
                )
            )

        return products