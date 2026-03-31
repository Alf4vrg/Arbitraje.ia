valid_categories = [
    "smartphones",
    "laptops",
    "mobile-accessories",
    "tablets",
    "tools",
    "auto-accessories",
]

def is_valid_category(category: str) -> bool:
    return category.lower() in valid_categories


def passes_minimum_margin(margin: float, minimum: float = 30.0) -> bool:
    return margin >= minimum