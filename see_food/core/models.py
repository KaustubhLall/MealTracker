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

    def __str__(self):
        return self.username


class Meal(models.Model):
    meal_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_name = models.CharField(max_length=255)
    time_of_consumption = models.DateTimeField()
    hunger_level = models.CharField(max_length=255, blank=True)
    exercise = models.CharField(max_length=255, blank=True)
    total_calories = models.FloatField(blank=True, default=0.0)
    total_fat = models.FloatField(blank=True, default=0.0)
    total_protein = models.FloatField(blank=True, default=0.0)
    total_carbs = models.FloatField(blank=True, default=0.0)
    total_sugar = models.FloatField(blank=True, default=0.0)

    def recalculate_macros(self):
        components = self.foodcomponent_set.all()
        self.total_calories = sum(component.total_calories for component in components)
        self.total_fat = sum(component.fat for component in components)
        self.total_protein = sum(component.protein for component in components)
        self.total_carbs = sum(component.carbs for component in components)
        self.total_sugar = sum(component.sugar for component in components)
        self.save()

    def __str__(self):
        return f"{self.meal_name} for {self.user.username} at {self.time_of_consumption}"


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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.meal.recalculate_macros()

    def __str__(self):
        return f"{self.food_name} ({self.brand})"


class HistoricalMeal(models.Model):
    historical_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_name = models.CharField(max_length=255)
    food_components = models.JSONField(default=list)
    brand_preferences = models.JSONField(default=dict)

    def __str__(self):
        return f"Historical {self.meal_name} for {self.user.username}"


class UserGoals(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="goals")
    fat_goal = models.IntegerField(default=0)
    carb_goal = models.IntegerField(default=0)
    protein_goal = models.IntegerField(default=0)
    calorie_goal = models.IntegerField(default=0)
    weight_goal = models.IntegerField(default=0)
    summary = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.user.username}'s goals"
