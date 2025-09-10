from rest_framework import serializers
from .models import Dietary, Ingredient, Meal, RecipeIngredient
from decimal import Decimal

class DietarySerializer(serializers.ModelSerializer):
    """
    Serializer for the Dietary model.
    Includes basic dietary info: id, name, description.
    """
    class Meta:
        model = Dietary
        fields = ["id", "name", "description"]

class IngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for the Ingredient model.
    Includes pricing, allergen, and nutritional fields.
    """
    class Meta:
        model = Ingredient
        fields = [
            "id", "name", "price_per_100g", "allergen",
            "energy_kj", "protein", "fat", "carbs", "fiber",
        ]

class RecipeIngredientInlineSerializer(serializers.ModelSerializer):
    """
    Inline serializer for RecipeIngredient, embedding the IngredientSerializer.
    Used to represent a single ingredient with its quantity in grams.
    """
    ingredient = IngredientSerializer()

    class Meta:
        model = RecipeIngredient
        fields = ["id", "ingredient", "quantity_g"]

class MealSerializer(serializers.ModelSerializer):
    """
    Serializer for the Meal model.
    Provides high-level info about a meal, including:
    - Dietary type (name only, read-only).
    - List of ingredient names.
    - Allergen list (deduplicated).
    - Computed totals for nutrition and cost.
    """
    dietary = serializers.CharField(source="dietary.name", read_only=True)  # only name
    ingredient_names = serializers.SerializerMethodField()
    allergens = serializers.SerializerMethodField() 
    
    total_energy_kj = serializers.SerializerMethodField()
    total_protein = serializers.SerializerMethodField()
    total_fat = serializers.SerializerMethodField()
    total_carbs = serializers.SerializerMethodField()
    total_fiber = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = Meal
        fields = [
            "id", "name", "description", "allergens", "dietary", "ingredient_names",
            "total_energy_kj", "total_protein", "total_fat",
            "total_carbs", "total_fiber", "total_cost"
        ]
        
    def get_ingredient_names(self, obj):
        """
        Return a list of ingredient names for the meal.
        """
        return list(
            obj.items.select_related("ingredient")
            .values_list("ingredient__name", flat=True)
        )

    def get_allergens(self, obj):
        """
        Return a list of allergens present in the meal.
        - Excludes null/empty allergen values.
        - Returns unique values only.
        """
        # Step 1: 拿到代碼列表
        return list(
            obj.items
              .exclude(ingredient__allergen__isnull=True)
              .exclude(ingredient__allergen__exact="")
              .values_list("ingredient__allergen", flat=True)
              .distinct()
        )
        # Step 2: 建立 choices_map {code: label}
        choices_map = dict(Ingredient._meta.get_field("allergen").choices)
        # Step 3: 轉成標籤（找不到的就回傳原始代碼）
        labels = [choices_map.get(c, c) for c in codes]
        return labels or None
        
    def get_total_energy_kj(self, obj):
        """
        Compute total energy (kJ) for the meal by summing all ingredients.
        """
        return self._sum_nutrition(obj, "energy_kj")

    def get_total_protein(self, obj):
        """
        Compute total protein (g) for the meal by summing all ingredients.
        """
        return self._sum_nutrition(obj, "protein")

    def get_total_fat(self, obj):
        """
        Compute total fat (g) for the meal by summing all ingredients.
        """
        return self._sum_nutrition(obj, "fat")

    def get_total_carbs(self, obj):
        """
        Compute total carbohydrates (g) for the meal by summing all ingredients.
        """
        return self._sum_nutrition(obj, "carbs")

    def get_total_fiber(self, obj):
        """
        Compute total fiber (g) for the meal by summing all ingredients.
        """
        return self._sum_nutrition(obj, "fiber")

    def get_total_cost(self, obj):
        """
        Compute total cost (NZD) for the meal.
        Formula: Σ(price_per_100g × (quantity_g / 100)).
        """
        total = Decimal("0.00")
        for item in obj.items.all():
            total += item.ingredient.price_per_100g * (item.quantity_g / Decimal("100"))
        return round(total, 2)

    def _sum_nutrition(self, obj, field_name):
        """
        Helper function to compute total nutrition (any field) for a meal.
        Args:
            obj (Meal): The meal instance.
            field_name (str): The field to sum ("energy_kj", "protein", etc.)
        Returns:
            Decimal: Rounded sum of that nutrition value across all ingredients.
        """
        total = Decimal("0.00")
        for item in obj.items.all():
            value_per_100g = getattr(item.ingredient, field_name) or Decimal("0.00")
            total += value_per_100g * (item.quantity_g / Decimal("100"))
        return round(total, 2)
