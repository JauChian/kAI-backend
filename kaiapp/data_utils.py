from kaiapp.models import Ingredient, Dietary

def load_ingredients():
    try:
        ingredients = Ingredient.objects.all()
        return [
            {
                "name": c.name,
                "price_per_100g": c.price_per_100g,
                "energy_kj": c.energy_kj

            }
            for c in ingredients
        ]
    except Exception as e:
        print(f"Failed to load charity cache: {e}")
        return []
        
def get_ingredients_for_dietary(dietary: str):
    """
    dietary 只接受: Standard, Vegetarian, Vegan, Halal, Gluten-free
    - Standard: 全部食材
    - 其他: 依 Ingredient.dietaries M2M 過濾
    """
    if not dietary or dietary.lower() == "standard":
        return Ingredient.objects.all().order_by("name")

    return (
        Ingredient.objects
        .filter(dietaries__name__iexact=dietary)
        .distinct()
        .order_by("name")
    )

def ingredients_to_prompt_block(qs):
    """
    把 QuerySet 轉成你 prompt 要的格式：
    “name, price_per_100g, energy_kj per 100g”
    """
    lines = []
    for i in qs:
        lines.append(f"{i.name}, {i.price_per_100g:.2f}, {i.energy_kj:.0f}")
    return "\n".join(lines)