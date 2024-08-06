from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.views import (
    UserViewSet,
    MealViewSet,
    FoodComponentViewSet,
    HistoricalMealViewSet,
    register,
    login,
    UserGoalsViewSet,
)

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"meals", MealViewSet, basename="meal")
router.register(r"foodcomponents", FoodComponentViewSet, basename="foodcomponent")
router.register(r"historicalmeals", HistoricalMealViewSet, basename="historicalmeal")
router.register(r"usergoals", UserGoalsViewSet, basename="user-goals")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/register/", register, name="register"),
    path("api/login/", login, name="login"),
]
