from django.test import TestCase

# Create your tests here.

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.hashers import make_password
from core.models import User, Meal, FoodComponent, HistoricalMeal
import json


class FoodTrackingAppE2ETests(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create(
            email="user@example.com",
            password=make_password("securepassword123"),
        )
        self.meal_url = reverse("meal-list")
        self.food_component_url = reverse("foodcomponent-list")
        self.historical_meal_url = reverse("historicalmeal-list")

        # User login to obtain auth token
        self.client.post(
            "/api/register/",
            {"email": "user@example.com", "password": "securepassword123"},
        )
        response = self.client.post(
            "/api/login/",
            {"email": "user@example.com", "password": "securepassword123"},
        )
        token = response.data["access"]  # Retrieve the access token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

    def test_user_registration(self):
        # Test user registration
        registration_data = {
            "email": "newuser@example.com",
            "password": "newpassword123",
        }
        response = self.client.post("/api/register/", registration_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_meal_creation_and_retrieval(self):
        # Test creating a meal
        meal_data = {
            "meal_name": "Lunch",
            "time_of_consumption": "2021-07-21T12:00:00Z",
            "user": self.user.user_id,
        }
        response = self.client.post(self.meal_url, meal_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test retrieving meals
        response = self.client.get(self.meal_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)  # Check that the meal was added

    def test_food_component_creation_and_retrieval(self):
        # Create a meal to attach components to
        meal = Meal.objects.create(
            meal_name="Dinner",
            time_of_consumption="2021-07-21T18:00:00Z",
            user=self.user,
        )

        # Test creating a food component
        component_data = {
            "meal": meal.meal_id,
            "food_name": "Potato",
            "brand": "Generic",
            "weight": 150,
            "fat": 0.2,
            "protein": 2,
            "carbs": 17,
            "sugar": 1,
            "micronutrients": json.dumps({"Vitamin C": "20mg"}),
        }
        response = self.client.post(self.food_component_url, component_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test retrieving food components
        response = self.client.get(self.food_component_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)  # Check that the component was added

    def test_historical_meal_creation_and_retrieval(self):
        # Test creating a historical meal
        historical_meal_data = {
            "meal_name": "Past Breakfast",
            "food_components": json.dumps(["Eggs", "Bacon", "Toast"]),
            "brand_preferences": json.dumps({"Brand": "Generic"}),
        }
        response = self.client.post(self.historical_meal_url, historical_meal_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test retrieving historical meals
        response = self.client.get(self.historical_meal_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            len(response.data) > 0
        )  # Check that the historical meal was added
