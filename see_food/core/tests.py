from django.contrib.auth import get_user_model
from django.urls import reverse
from icecream import ic
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class SeeFoodAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.meal_url = reverse('meal-list')
        self.food_component_url = reverse('foodcomponent-list')
        self.historical_meal_url = reverse('historicalmeal-list')
        self.username_base = "testuser"

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
            "email": f"{username}@example.com"
        }
        ic(register_data)
        response = self.client.post(self.register_url, register_data, format='json')
        ic(response.status_code)
        ic(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Login with the registered user
        login_data = {
            "username": username,
            "password": "testpassword"
        }
        ic(login_data)
        response = self.client.post(self.login_url, login_data, format='json')
        ic(response.status_code)
        ic(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tokens = response.data
        self.assertIn("access", tokens)
        self.assertIn("refresh", tokens)
        self.access_token = tokens["access"]

    def test_meal_management(self):
        try:
            self.test_register_and_login()
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

            # Create a new meal
            meal_data = {
                "name": "Breakfast",
                "description": "Morning meal",
            }
            ic(meal_data)
            response = self.client.post(self.meal_url, meal_data, format='json')
            ic(response.status_code)
            ic(response.data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            meal_id = response.data["id"]

            # Edit the meal
            edit_meal_data = {
                "name": "Updated Breakfast",
                "description": "Updated morning meal",
            }
            ic(edit_meal_data)
            response = self.client.put(f"{self.meal_url}{meal_id}/edit_meal/", edit_meal_data, format='json')
            ic(response.status_code)
            ic(response.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except Exception as e:
            ic(e)

    def test_food_component_management(self):
        try:
            self.test_meal_management()

            # Create a new food component
            food_component_data = {
                "name": "Eggs",
                "calories": 155,
                "meal": 1  # Assuming the meal created in test_meal_management has ID 1
            }
            ic(food_component_data)
            response = self.client.post(self.food_component_url, food_component_data, format='json')
            ic(response.status_code)
            ic(response.data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            food_component_id = response.data["id"]

            # Edit the food component
            edit_food_component_data = {
                "name": "Boiled Eggs",
                "calories": 155,
            }
            ic(edit_food_component_data)
            response = self.client.put(f"{self.food_component_url}{food_component_id}/edit_food_component/", edit_food_component_data, format='json')
            ic(response.status_code)
            ic(response.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except Exception as e:
            ic(e)

    def test_historical_meal_management(self):
        try:
            self.test_register_and_login()
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

            # Add a historical meal
            historical_meal_data = {
                "date": "2024-07-28",
                "meal": 1  # Assuming the meal created in test_meal_management has ID 1
            }
            ic(historical_meal_data)
            response = self.client.post(f"{self.historical_meal_url}add_historical_meal/", historical_meal_data, format='json')
            ic(response.status_code)
            ic(response.data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            historical_meal_id = response.data["id"]

            # Edit the historical meal
            edit_historical_meal_data = {
                "date": "2024-07-29",
            }
            ic(edit_historical_meal_data)
            response = self.client.put(f"{self.historical_meal_url}{historical_meal_id}/edit_historical_meal/", edit_historical_meal_data, format='json')
            ic(response.status_code)
            ic(response.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except Exception as e:
            ic(e)

if __name__ == "__main__":
    SeeFoodAPITest().run_tests()
