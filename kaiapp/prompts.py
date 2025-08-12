def filter_ingredients_by_dietary(ingredients_list, dietary):
    """
    根據 dietary 過濾食材
    ingredients_list: list[dict]，每個元素至少要有 'name' 和 'dietary' 屬性
    dietary: 'Standard' | 'Vegetarian' | 'Vegan' | 'Halal' | 'Gluten-free'
    """
    if dietary == "Standard":
        return ingredients_list  # 不過濾，所有食材可用

    return [ing for ing in ingredients_list if ing.get("dietary") == dietary]


def build_menu_prompt(
    ingredients_block: str,
    batch_size: int = 10,
    dietary: str = "Standard",
    energy_min: int = 2200,
    price_min: float = 2.50,
    price_max: float = 3.00,
    weight_min: int = 200,
    weight_max: int = 350,
    items_min: int = 5,
    items_max: int = 6,
):
    cuisine_cues = "Teriyaki, Karaage, Sichuan, Satay, Miso, Kiwi, Tex-Mex, Mediterranean, Italian, Japanese, Burger, Indian, Stir-Fry, Chinese, Viet, Māori, Islander"
    suffixes = "Bowl, Box, Wrap, Stack, Smash, Blaze, Boost, Fuel, Feast"

    return f"""
You are a **school-lunch menu generator**. Produce exactly {batch_size} menus using ONLY the ingredients listed below.
You must choose quantities so every menu meets **all numeric constraints**. Output **valid JSON only**.

### Hard Constraints (apply to EACH menu)
- Total energy: **≥ {energy_min} kJ**
- Total cost: **> {price_min:.2f} and ≤ {price_max:.2f} NZD**
- Total weight: **{weight_min}–{weight_max} g**
- Ingredient count: **{items_min}–{items_max} items**
- Dietary type: **{dietary}** (only use ingredients that comply)
- Use **names exactly as listed** (case & spelling). **Do not invent** ingredients.

### Composition Rules (to improve pass rate)
- Include **one primary carb** (Rice / Pasta / Potato / Sweet Potato / Bread if present).
- Include **one primary protein** (e.g., Chicken Breast, Beef Mince, Pork Loin, Salmon, Shrimp, Egg, or Tofu).
  - Vegetarian: no meat or seafood. Vegan: no meat/seafood/egg/dairy. Halal: no pork. Gluten-free: no Flour/Pasta.
- Add **1–3 vegetables** for balance (e.g., Broccoli, Carrot, Onion, Spinach, Mushroom, Bell Pepper, Cabbage, Corn, Peas, Tomato, Lettuce, Cucumber, Zucchini).
- Optionally include **a small energy booster** (Olive Oil 5–12 g, or Cheddar Cheese 10–20 g if allowed) to help reach kJ.

### Quantity Guidelines (choose within ranges, then fine-tune)
- Carb base: **Rice 150–220 g** (cooked) / **Pasta (dry) 70–100 g** / **Potato 180–260 g** / **Sweet Potato 160–240 g**
- Protein: **Chicken/Beef/Pork 90–150 g**, **Salmon 80–120 g**, **Shrimp 90–140 g**, **Tofu 140–220 g**, **Egg 50–100 g**
- Vegetables (each): **40–120 g**
- Boosters: **Olive Oil 5–12 g**, **Cheddar Cheese 10–20 g** (only if dietary allows)

### Batch Diversity
Across the {batch_size} menus:
- Mix cuisines: {cuisine_cues}.
- Vary bases (rice/pasta/potato) and proteins. **Avoid repeating the exact same ingredient set**.
- Names and descriptions must be distinct.

### Naming (audience: 13–19)
- English, Title Case, **3–6 words**.
- End with **one** of: {suffixes}.
- Optionally include a cuisine cue (e.g., Teriyaki, Tex-Mex, Māori, Italian, Sichuan…).
- Avoid boring “X with Y” patterns.

### Description
- **≤ 16 words**, hype-y but clear (e.g., “crispy tofu, miso glaze, veggie crunch”).

### Provided Ingredients
Format per line: `name, price_per_100g, energy_kj_per_100g`
{ingredients_block}

### Output (JSON only)
{{
  "menus": [
    {{
      "meal_name": "string",
      "description": "string (≤16 words)",
      "dietary": "{dietary}",
      "items": [
        {{ "name": "IngredientName", "quantity_g": int }}
      ]
    }}
  ]
}}

### Validation Before You Output (think silently, then output JSON)
For each menu:
1) Compute **weight** (sum of quantity_g). Must be within **{weight_min}–{weight_max} g**.
2) Compute **energy_kj** = Σ(ingredient.energy_kj_per_100g × quantity_g / 100). Must be **≥ {energy_min}**.
3) Compute **cost_nzd** = Σ(ingredient.price_per_100g × quantity_g / 100). Must be **> {price_min:.2f} and ≤ {price_max:.2f}**.
4) If any check fails, **adjust quantities**:
   - First, adjust **carb base** ±10–30 g.
   - Then, adjust **protein** ±10–20 g.
   - If energy low, add **booster** (Olive Oil +2–5 g) if allowed; if cost too high, reduce the most expensive item first.
   - Keep total weight within range.
5) Ensure ingredient names **exactly match** the list, comply with **{dietary}**, and each menu uses **{items_min}–{items_max} items**.

Return **only** the final JSON. No comments or extra text.
"""


