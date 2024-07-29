from rest_framework import serializers
from .models import User, Meal, FoodComponent, HistoricalMeal


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "email", "password"]


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = "__all__"


class FoodComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodComponent
        fields = "__all__"


class HistoricalMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalMeal
        fields = "__all__"
