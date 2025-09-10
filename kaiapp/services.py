# kaiapp/services.py
from decimal import Decimal
from .models import Ingredient

def compute_totals(items):
    """
    Compute total energy (kJ) and cost for a given list of ingredients.
    
    Args:
        items (list[dict]): List of dicts in the form:
            [{"name": "Rice", "quantity_g": 180}, ...]
    
    Returns:
        tuple: (total_energy_kj, total_cost), both rounded to 2 decimals.
    
    Raises:
        ValueError: If an ingredient cannot be found in the database.
    """
    total_energy = Decimal("0")
    total_cost = Decimal("0")
    for it in items:
        ing = Ingredient.objects.filter(name__iexact=it["name"]).first()
        if not ing:
            raise ValueError(f"Ingredient not found: {it['name']}")
        qty = Decimal(str(it["quantity_g"]))
        # Energy and cost are scaled by quantity (per 100g basis)
        total_energy += (ing.energy_kj * qty / Decimal("100"))
        total_cost   += (ing.price_per_100g * qty / Decimal("100"))
    # Round to 2 decimals for display
    return round(total_energy, 2), round(total_cost, 2)

def validate_menu(items, min_kj=2500, max_cost=3, min_g=200, max_g=350):
    """
    Validate a menu based on simple nutrition and budget rules.
    
    Rules:
        - Total weight must be between min_g and max_g (grams)
        - Total energy must be >= min_kj (kJ)
        - Total cost must be <= max_cost (currency units)
    
    Args:
        items (list[dict]): List of dicts in the form:
            [{"name": "Rice", "quantity_g": 180}, ...]
        min_kj (int|float): Minimum required energy in kJ (default=2500)
        max_cost (int|float): Maximum allowed cost (default=3)
        min_g (int|float): Minimum total weight in grams (default=200)
        max_g (int|float): Maximum total weight in grams (default=350)
    
    Returns:
        tuple: (is_valid, result)
            - If valid: (True, {"total_kj": x, "total_cost": y})
            - If invalid: (False, error_message)
    """
    total_g = sum(Decimal(str(i["quantity_g"])) for i in items)
    if not (Decimal(str(min_g)) <= total_g <= Decimal(str(max_g))):
        return False, f"total_g={total_g} not in [{min_g},{max_g}]"
    try:
        total_kj, total_cost = compute_totals(items)
    except ValueError as e:
        return False, str(e)
    if total_kj < Decimal(str(min_kj)):
        return False, f"energy_kj={total_kj} < {min_kj}"
    if total_cost > Decimal(str(max_cost)):
        return False, f"cost={total_cost} > {max_cost}"
    return True, {"total_kj": total_kj, "total_cost": total_cost}
