# kaiapp/services.py
from decimal import Decimal
from .models import Ingredient

def compute_totals(items):
    """
    items: [{"name": "Rice", "quantity_g": 180}, ...]
    回傳: (total_energy_kj, total_cost)
    """
    total_energy = Decimal("0")
    total_cost = Decimal("0")
    for it in items:
        ing = Ingredient.objects.filter(name__iexact=it["name"]).first()
        if not ing:
            raise ValueError(f"Ingredient not found: {it['name']}")
        qty = Decimal(str(it["quantity_g"]))
        total_energy += (ing.energy_kj * qty / Decimal("100"))
        total_cost   += (ing.price_per_100g * qty / Decimal("100"))
    # 四捨五入顯示
    return round(total_energy, 2), round(total_cost, 2)

def validate_menu(items, min_kj=2500, max_cost=3, min_g=200, max_g=350):
    """
    基本規則：能量>=min_kj、成本<=max_cost、總重量在區間內。
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
