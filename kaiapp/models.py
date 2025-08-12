from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator

# Common allergens list for standardized choices
KNOWN_ALLERGENS = [
    ("peanut", "peanut"),
    ("soy", "soy"),
    ("milk", "milk"),
    ("egg", "egg"),
    ("wheat", "wheat"),
    ("gluten", "gluten"),
    ("tree-nut", "tree-nut"),
    ("almond", "almond"),
    ("cashew", "cashew"),
    ("pistachio", "pistachio"),
    ("walnut", "walnut"),
    ("sesame", "sesame"),
    ("fish", "fish"),
    ("shellfish", "shellfish"),
]

class Dietary(models.Model):
    """
    Represents a dietary category or restriction.
    Examples: standard, vegan, vegetarian, halal, gluten-free.
    """
    name = models.CharField(max_length=64)  # Short dietary name
    description = models.CharField(max_length=255, blank=True)  # Optional description

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Represents a single ingredient with nutritional information.
    Price is standardized per 100g to allow consistent cost calculation.
    """
    name = models.CharField(max_length=120, unique=True)
    price_per_100g = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Price per 100 g"
    )
    allergen = models.SlugField(max_length=50, choices=KNOWN_ALLERGENS, blank=True)
    dietaries = models.ManyToManyField(Dietary, blank=True, related_name="ingredients")

    # per 100 g nutrition (in kJ)
    energy_kj = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # kJ / 100g
    protein   = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # g / 100g
    fat       = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # g / 100g
    carbs     = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # g / 100g
    fiber     = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # g / 100g

    def __str__(self):
        return self.name


class Meal(models.Model):
    """
    Represents a complete meal recipe.
    Each meal may belong to a single dietary category
    (if multiple, change FK to ManyToMany).
    Ingredients are linked via RecipeIngredient to store quantities.
    """
    name = models.CharField(max_length=160, unique=True)  # Meal name
    description = models.TextField(blank=True)  # Optional description
    dietary = models.ForeignKey(  # Linked dietary type
        Dietary, null=True, blank=True, on_delete=models.PROTECT
    )
    ingredients = models.ManyToManyField(  # Ingredient list with quantities
        Ingredient,
        through="RecipeIngredient",
        related_name="meals",
    )

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """
    Intermediate model between Meal and Ingredient.
    Stores the exact quantity of each ingredient used in a meal.
    """
    recipe = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="items")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    quantity_g = models.DecimalField(  # Quantity in grams
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"], name="uniq_recipe_ingredient"
            )
        ]

    def __str__(self):
        return f"{self.ingredient.name} in {self.recipe.name} ({self.quantity_g} g)"
