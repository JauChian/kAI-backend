from rest_framework import viewsets
from .models import Meal
from .serializers import MealSerializer

class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer