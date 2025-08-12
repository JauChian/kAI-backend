from rest_framework.routers import DefaultRouter
from kaiapp.viewsets import MealViewSet
from django.urls import path
from .views import GenerateMenusView, MonthlyMenuView

router = DefaultRouter()
router.register(r'meals',MealViewSet)

urlpatterns= urlpatterns = [
    *router.urls,
    path('generate-menus/', GenerateMenusView.as_view(), name='generate-menus'),
    path("monthly-menu/", MonthlyMenuView.as_view(), name="monthly-menu"),
]