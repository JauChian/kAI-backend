from rest_framework import serializers
from .models import Dietary, Ingredient, Meal, RecipeIngredient
from decimal import Decimal

class DietarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dietary
        fields = ["id", "name", "description"]

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = [
            "id", "name", "price_per_100g", "allergen",
            "energy_kj", "protein", "fat", "carbs", "fiber",
        ]

class RecipeIngredientInlineSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = RecipeIngredient
        fields = ["id", "ingredient", "quantity_g"]

class MealSerializer(serializers.ModelSerializer):
    dietary = serializers.CharField(source="dietary.name", read_only=True)  # only name
    ingredient_names = serializers.SerializerMethodField()
    
    total_energy_kj = serializers.SerializerMethodField()
    total_protein = serializers.SerializerMethodField()
    total_fat = serializers.SerializerMethodField()
    total_carbs = serializers.SerializerMethodField()
    total_fiber = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = Meal
        fields = [
            "id", "name", "description", "dietary", "ingredient_names",
            "total_energy_kj", "total_protein", "total_fat",
            "total_carbs", "total_fiber", "total_cost"
        ]

    def get_ingredient_names(self, obj):
        return list(
            obj.items.select_related("ingredient")
            .values_list("ingredient__name", flat=True)
        )
        
    def get_total_energy_kj(self, obj):
        return self._sum_nutrition(obj, "energy_kj")

    def get_total_protein(self, obj):
        return self._sum_nutrition(obj, "protein")

    def get_total_fat(self, obj):
        return self._sum_nutrition(obj, "fat")

    def get_total_carbs(self, obj):
        return self._sum_nutrition(obj, "carbs")

    def get_total_fiber(self, obj):
        return self._sum_nutrition(obj, "fiber")

    def get_total_cost(self, obj):
        total = Decimal("0.00")
        for item in obj.items.all():
            total += item.ingredient.price_per_100g * (item.quantity_g / Decimal("100"))
        return round(total, 2)

    def _sum_nutrition(self, obj, field_name):
        total = Decimal("0.00")
        for item in obj.items.all():
            value_per_100g = getattr(item.ingredient, field_name) or Decimal("0.00")
            total += value_per_100g * (item.quantity_g / Decimal("100"))
        return round(total, 2)
