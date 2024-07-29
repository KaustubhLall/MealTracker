from django.db import models

# Create your models here.
from django.db import models
import uuid
import json


class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)


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
    meal_name = models.CharField(max_length=255)
    food_components = models.JSONField(default=list)
    brand_preferences = models.JSONField(default=dict)
