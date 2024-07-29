import uuid

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        blank=True,
        help_text=(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_set",
        blank=True,
        help_text="Specific permissions for this user.",
        related_query_name="user",
    )


class Meal(models.Model):
    meal_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_name = models.CharField(max_length=255)
    time_of_consumption = models.DateTimeField()
    hunger_level = models.CharField(max_length=255, blank=True)
    exercise = models.CharField(max_length=255, blank=True)
    total_calories = models.CharField(max_length=255, blank=True)


class FoodComponent(models.Model):
    component_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, blank=True)
    weight = models.FloatField()
    fat = models.FloatField()
    protein = models.FloatField()
    carbs = models.FloatField()
    sugar = models.FloatField()
    micronutrients = models.JSONField(default=dict)
    total_calories = models.FloatField()


class HistoricalMeal(models.Model):
    historical_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_name = models.CharField(max_length=255)
    food_components = models.JSONField(default=list)
    brand_preferences = models.JSONField(default=dict)
