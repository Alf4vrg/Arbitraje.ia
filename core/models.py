from dataclasses import dataclass


@dataclass
class Product:
    source: str
    title: str
    category: str
    price: float
    currency: str
    rating: float
    discount_percent: float
    image_url: str
    product_url: str

    demand_score: float = 0.0
    base_price: float = 0.0
    estimated_sale_price: float = 0.0
    estimated_profit: float = 0.0
    estimated_margin: float = 0.0
    buy_index: float = 0.0
    initial_decision: str = "❌ DESCARTAR"

    real_sale_price: float = 0.0
    real_profit: float = 0.0
    real_margin: float = 0.0
    validation_status: str = "❓ SIN VALIDAR"
    final_decision: str = "❌ DESCARTAR"
    suggested_capital: float = 0.0