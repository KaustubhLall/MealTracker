from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from core.models import UserGoals, Meal


class SeeFoodAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.meal_url = reverse("meal-list")
        self.food_component_url = reverse("foodcomponent-list")
        self.historical_meal_url = reverse("historicalmeal-list")
        self.goals_url = reverse("user-goals-list")
        self.username_base = "testuser"

        # Register and login a test user
        self.test_register_and_login()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

    def create_sequential_user(self):
        index = 0
        while True:
            username = f"{self.username_base}{index}"
            if not get_user_model().objects.filter(username=username).exists():
                return username
            index += 1

    def test_register_and_login(self):
        # Register a new user with a unique username
        username = self.create_sequential_user()
        register_data = {
            "username": username,
            "password": "testpassword",
            "email": f"{username}@example.com",
        }
        response = self.client.post(self.register_url, register_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(f"Registration response data: {response.data}")

        # Manually authenticate the user
        user = authenticate(username=username, password="testpassword")
        print(f"Manual authentication for {username}: {user}")

        # Login with the registered user
        login_data = {"username": username, "password": "testpassword"}
        response = self.client.post(self.login_url, login_data, format="json")
        print(f"Login response status code: {response.status_code}")
        print(f"Login response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tokens = response.data
        self.assertIn("access", tokens)
        self.assertIn("refresh", tokens)
        self.access_token = tokens["access"]
        self.user = user

    def test_meal_management(self):
        # Create a new meal
        meal_data = {
            "meal_name": "Breakfast",
            "time_of_consumption": "2024-07-29T08:30:00Z",
            "hunger_level": "High",
            "exercise": "None",
            "total_calories": "500",
            "user": self.user.user_id,
        }
        response = self.client.post(self.meal_url, meal_data, format="json")
        print(f"Meal creation response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        meal_id = response.data["meal_id"]

        # Edit the meal
        edit_meal_data = {"meal_name": "Updated Breakfast", "hunger_level": "Moderate"}
        response = self.client.put(
            f"{self.meal_url}{meal_id}/edit_meal/", edit_meal_data, format="json"
        )
        print(f"Meal update response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_food_component_management(self):
        # Create a new meal
        meal_data = {
            "meal_name": "Lunch",
            "time_of_consumption": "2024-07-29T13:00:00Z",
            "hunger_level": "Moderate",
            "exercise": "Light",
            "total_calories": "0",
            "user": self.user.user_id,
        }
        response = self.client.post(self.meal_url, meal_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        meal_id = response.data["meal_id"]

        # Create a new food component
        food_component_data = {
            "meal": meal_id,
            "food_name": "Chicken",
            "brand": "Brand A",
            "weight": 200,
            "fat": 10,
            "protein": 30,
            "carbs": 0,
            "sugar": 0,
            "micronutrients": {"vitamin_c": 0},
            "total_calories": 200,
        }
        response = self.client.post(
            self.food_component_url, food_component_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check recalculated meal macros
        meal = Meal.objects.get(meal_id=meal_id)
        self.assertEqual(meal.total_calories, 200)
        self.assertEqual(meal.total_fat, 10)
        self.assertEqual(meal.total_protein, 30)
        self.assertEqual(meal.total_carbs, 0)
        self.assertEqual(meal.total_sugar, 0)

        # Edit the food component
        component_id = response.data["component_id"]
        edit_food_component_data = {
            "food_name": "Grilled Chicken",
            "weight": 250,
            "fat": 12,
            "protein": 32,
            "carbs": 5,
            "sugar": 1,
            "total_calories": 250,
        }
        response = self.client.put(
            f"{self.food_component_url}{component_id}/edit_food_component/",
            edit_food_component_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check recalculated meal macros after update
        meal.refresh_from_db()
        self.assertEqual(meal.total_calories, 250)
        self.assertEqual(meal.total_fat, 12)
        self.assertEqual(meal.total_protein, 32)
        self.assertEqual(meal.total_carbs, 5)
        self.assertEqual(meal.total_sugar, 1)

    def test_historical_meal_management(self):
        # Add a historical meal
        historical_meal_data = {
            "meal_name": "Dinner",
            "food_components": [
                {
                    "food_name": "Salad",
                    "brand": "Brand B",
                    "weight": 150,
                    "fat": 5,
                    "protein": 2,
                    "carbs": 20,
                    "sugar": 5,
                    "micronutrients": {"vitamin_a": 50},
                    "total_calories": 100,
                }
            ],
            "brand_preferences": {"Brand A": 2, "Brand B": 5},
            "user": self.user.user_id,
        }
        response = self.client.post(
            f"{self.historical_meal_url}add_historical_meal/",
            historical_meal_data,
            format="json",
        )
        print(f"Historical meal creation response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        historical_meal_id = response.data["historical_id"]

        # Edit the historical meal
        edit_historical_meal_data = {"meal_name": "Updated Dinner"}
        response = self.client.put(
            f"{self.historical_meal_url}{historical_meal_id}/edit_historical_meal/",
            edit_historical_meal_data,
            format="json",
        )
        print(f"Historical meal update response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # List historical meals
        response = self.client.get(
            f"{self.historical_meal_url}list_historical_meals/", format="json"
        )
        print(f"List historical meals response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_create_user_goals(self):
        # Test creating user goals
        data = {"goals_input": "I want to reduce carbs and increase protein"}
        response = self.client.post(self.goals_url, data, format="json")
        print(f"User goals creation response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["fat_goal"], 42)

        # Check if summary includes the input
        self.assertIn(
            "I want to reduce carbs and increase protein", response.data["summary"]
        )

    def test_get_user_goals(self):
        # Ensure user goals are created first
        self.test_create_user_goals()

        # Retrieve the user goals
        response = self.client.get(self.goals_url, format="json")
        print(f"User goals retrieval response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("fat_goal", response.data[0])

    def test_update_user_goals(self):
        # Ensure user goals are created first
        self.test_create_user_goals()

        # Update the user goals
        new_goals_input = {"goals_input": "I want to increase carbs and reduce protein"}
        user_goals_id = UserGoals.objects.get(user=self.user).id
        response = self.client.put(
            f"{self.goals_url}{user_goals_id}/", new_goals_input, format="json"
        )
        print(f"User goals update response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if summary includes the new input
        self.assertIn(
            "I want to reduce carbs and increase protein", response.data["summary"]
        )
        self.assertIn(
            "I want to increase carbs and reduce protein", response.data["summary"]
        )

        # Assuming parsing logic will change values appropriately
        self.assertEqual(response.data["carb_goal"], 42)
        self.assertEqual(response.data["protein_goal"], 42)


if __name__ == "__main__":
    SeeFoodAPITest().run_tests()
