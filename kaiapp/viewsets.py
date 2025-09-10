from rest_framework import viewsets
from .models import Meal
from .serializers import MealSerializer

class MealViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Meal model.

    Provides full CRUD API endpoints automatically:
    - GET /meals/        → list all meals
    - GET /meals/{id}/   → retrieve a single meal
    - POST /meals/       → create a new meal
    - PUT /meals/{id}/   → update an existing meal (full update)
    - PATCH /meals/{id}/ → update an existing meal (partial update)
    - DELETE /meals/{id}/→ delete a meal

    Uses MealSerializer to control how Meal objects are represented.
    """
    queryset = Meal.objects.all()
    serializer_class = MealSerializer