import logging

from rest_framework import serializers

from .models import User, Meal, FoodComponent, HistoricalMeal, UserGoals

logger = logging.getLogger("see_food")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"], email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        logger.debug(f"Creating user with username: {user.username}")
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        password = validated_data.get("password", None)
        if password:
            instance.set_password(password)
            logger.debug(f"Updating user with username: {instance.username}")
        instance.save()
        return instance


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


class UserGoalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGoals
        fields = [
            "fat_goal",
            "carb_goal",
            "protein_goal",
            "calorie_goal",
            "weight_goal",
            'summary'
        ]
