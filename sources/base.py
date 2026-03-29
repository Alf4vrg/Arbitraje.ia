from abc import ABC, abstractmethod
from typing import List
from core.models import Product


class ProductSource(ABC):
    @abstractmethod
    def fetch_products(self, query: str = "") -> List[Product]:
        raise NotImplementedError