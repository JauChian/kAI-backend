from django.contrib import admin
from decimal import Decimal
# Register your models here.
from django.contrib import admin
from .models import Dietary, Ingredient, Meal, RecipeIngredient

@admin.register(Dietary)
class DietaryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "price_per_100g", "allergen",
                    "energy_kj", "protein", "fat", "carbs", "fiber")
    list_filter = ("allergen", "dietaries")
    search_fields = ("name",)

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    autocomplete_fields = ("ingredient",)

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = (
        "name", "dietary", "total_energy_kj", "total_protein",
        "total_fat", "total_carbs", "total_fiber", "total_cost"
    )
    search_fields = ("name",)
    list_filter = ("dietary",)
    inlines = [RecipeIngredientInline]

    def total_energy_kj(self, obj):
        return self._sum_nutrition(obj, "energy_kj")
    total_energy_kj.short_description = "Energy (kJ)"

    def total_protein(self, obj):
        return self._sum_nutrition(obj, "protein")
    total_protein.short_description = "Protein (g)"

    def total_fat(self, obj):
        return self._sum_nutrition(obj, "fat")
    total_fat.short_description = "Fat (g)"

    def total_carbs(self, obj):
        return self._sum_nutrition(obj, "carbs")
    total_carbs.short_description = "Carbs (g)"

    def total_fiber(self, obj):
        return self._sum_nutrition(obj, "fiber")
    total_fiber.short_description = "Fiber (g)"

    def total_cost(self, obj):
        total = Decimal("0.00")
        for item in obj.items.all():
            total += item.ingredient.price_per_100g * (item.quantity_g / Decimal("100"))
        return round(total, 2)
    total_cost.short_description = "Cost ($)"

    def _sum_nutrition(self, obj, field_name):
        total = Decimal("0.00")
        for item in obj.items.all():
            value_per_100g = getattr(item.ingredient, field_name) or Decimal("0.00")
            total += value_per_100g * (item.quantity_g / Decimal("100"))
        return round(total, 2)
