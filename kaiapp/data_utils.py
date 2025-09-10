from kaiapp.models import Ingredient, Dietary

def load_ingredients():
    """
    Load all ingredients from the database and return them as a list of dicts.
    Each dict includes: name, price_per_100g, and energy_kj.
    """
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
        # Log error if the query fails
        print(f"Failed to load charity cache: {e}")
        return []
        
def get_ingredients_for_dietary(dietary: str):
    """
    Filter ingredients by dietary category.
    Accepted values: Standard, Vegetarian, Vegan, Halal, Gluten-free
    
    - Standard: returns all ingredients
    - Others: filters by Ingredient.dietaries ManyToMany relation
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
    Convert a QuerySet of ingredients into a string block
    suitable for feeding into a prompt.

    Format per line: "name, price_per_100g, energy_kj per 100g"
    Example:
    Brown Rice, 0.50, 1500
    Chicken Breast, 1.20, 1100
    """
    lines = []
    for i in qs:
        lines.append(f"{i.name}, {i.price_per_100g:.2f}, {i.energy_kj:.0f}")
    return "\n".join(lines)