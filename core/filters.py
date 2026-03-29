VALID_CATEGORIES = {
    "smartphones",
    "laptops",
    "mobile-accessories",
    "tablets",
}


def is_valid_category(category: str) -> bool:
    return category.lower() in VALID_CATEGORIES


def passes_minimum_margin(margin: float, minimum: float = 30.0) -> bool:
    return margin >= minimum