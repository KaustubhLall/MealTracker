import logging

from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Meal, FoodComponent, HistoricalMeal, UserGoals
from .serializers import (
    UserSerializer,
    MealSerializer,
    FoodComponentSerializer,
    HistoricalMealSerializer,
    UserGoalsSerializer,
)

User = get_user_model()
logger = logging.getLogger("see_food")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.user_id)


@api_view(["POST"])
def register(request):
    logger.debug(f"{register.__name__}: Received registration request.")
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        logger.debug(
            f"{register.__name__}: User registered successfully with username: {user.username}."
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        logger.debug(
            f"{register.__name__}: Registration failed with errors: {serializer.errors}."
        )
        return Response(
            {
                "message": "Registration failed due to invalid data.",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or password is None:
        logger.debug(f"{login.__name__}: Missing username or password in the request.")
        return Response(
            {"error": "Please provide both username and password."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    logger.debug(f"{login.__name__}: Attempting to authenticate user: {username}.")
    user = authenticate(username=username, password=password)
    if user:
        logger.debug(f"{login.__name__}: User authenticated successfully: {username}.")
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )

    logger.debug(f"{login.__name__}: Invalid credentials for user: {username}.")
    return Response(
        {
            "error": "Invalid Credentials",
            "message": "The username or password you entered is incorrect. Please try again.",
        },
        status=status.HTTP_401_UNAUTHORIZED,
    )


class MealViewSet(viewsets.ModelViewSet):
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Meal.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        logger.debug(
            f"{self.__class__.__name__}.{self.create.__name__}: Creating a new meal."
        )
        data = request.data.copy()
        data["user"] = request.user.user_id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            logger.debug(
                f"{self.__class__.__name__}.{self.create.__name__}: Meal created successfully."
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.debug(
                f"{self.__class__.__name__}.{self.create.__name__}: Meal creation failed with errors: {serializer.errors}."
            )
            return Response(
                {
                    "message": "Meal creation failed due to invalid data.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["put"])
    def edit_meal(self, request, pk=None):
        logger.debug(
            f"{self.__class__.__name__}.{self.edit_meal.__name__}: Editing meal with ID: {pk}."
        )
        meal = self.get_object()
        serializer = MealSerializer(meal, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.debug(
                f"{self.__class__.__name__}.{self.edit_meal.__name__}: Meal updated successfully."
            )
            return Response(serializer.data)
        else:
            logger.debug(
                f"{self.__class__.__name__}.{self.edit_meal.__name__}: Meal update failed with errors: {serializer.errors}."
            )
            return Response(
                {
                    "message": "Meal update failed due to invalid data.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class FoodComponentViewSet(viewsets.ModelViewSet):
    serializer_class = FoodComponentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FoodComponent.objects.filter(meal__user=self.request.user)

    def create(self, request, *args, **kwargs):
        logger.debug(
            f"{self.__class__.__name__}.{self.create.__name__}: Creating a new food component."
        )
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            food_component = serializer.save()
            food_component.meal.recalculate_macros()
            logger.debug(
                f"{self.__class__.__name__}.{self.create.__name__}: Food component created and macros recalculated."
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.debug(
                f"{self.__class__.__name__}.{self.create.__name__}: Food component creation failed with errors: {serializer.errors}."
            )
            return Response(
                {
                    "message": "Food component creation failed due to invalid data.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["put"])
    def edit_food_component(self, request, pk=None):
        logger.debug(
            f"{self.__class__.__name__}.{self.edit_food_component.__name__}: Editing food component with ID: {pk}."
        )
        food_component = self.get_object()
        serializer = FoodComponentSerializer(
            food_component, data=request.data, partial=True
        )
        if serializer.is_valid():
            food_component = serializer.save()
            food_component.meal.recalculate_macros()
            logger.debug(
                f"{self.__class__.__name__}.{self.edit_food_component.__name__}: Food component updated and macros recalculated."
            )
            return Response(serializer.data)
        else:
            logger.debug(
                f"{self.__class__.__name__}.{self.edit_food_component.__name__}: Food component update failed with errors: {serializer.errors}."
            )
            return Response(
                {
                    "message": "Food component update failed due to invalid data.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class HistoricalMealViewSet(viewsets.ModelViewSet):
    serializer_class = HistoricalMealSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HistoricalMeal.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        logger.debug(
            f"{self.__class__.__name__}.{self.create.__name__}: Creating a new historical meal."
        )
        data = request.data.copy()
        data["user"] = request.user.user_id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            logger.debug(
                f"{self.__class__.__name__}.{self.create.__name__}: Historical meal created successfully."
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.debug(
                f"{self.__class__.__name__}.{self.create.__name__}: Historical meal creation failed with errors: {serializer.errors}."
            )
            return Response(
                {
                    "message": "Historical meal creation failed due to invalid data.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["post"])
    def add_historical_meal(self, request):
        logger.debug(
            f"{self.__class__.__name__}.{self.add_historical_meal.__name__}: Adding a historical meal."
        )
        return self.create(request)

    @action(detail=False, methods=["get"])
    def list_historical_meals(self, request):
        logger.debug(
            f"{self.__class__.__name__}.{self.list_historical_meals.__name__}: Listing historical meals."
        )
        historical_meals = self.get_queryset()
        serializer = HistoricalMealSerializer(historical_meals, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["put"])
    def edit_historical_meal(self, request, pk=None):
        logger.debug(
            f"{self.__class__.__name__}.{self.edit_historical_meal.__name__}: Editing historical meal with ID: {pk}."
        )
        historical_meal = self.get_object()
        serializer = HistoricalMealSerializer(
            historical_meal, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            logger.debug(
                f"{self.__class__.__name__}.{self.edit_historical_meal.__name__}: Historical meal updated successfully."
            )
            return Response(serializer.data)
        else:
            logger.debug(
                f"{self.__class__.__name__}.{self.edit_historical_meal.__name__}: Historical meal update failed with errors: {serializer.errors}."
            )
            return Response(
                {
                    "message": "Historical meal update failed due to invalid data.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserGoalsViewSet(viewsets.ModelViewSet):
    serializer_class = UserGoalsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserGoals.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        logger.debug(
            f"{self.__class__.__name__}.{self.create.__name__}: Creating user goals."
        )
        goals_input = request.data.get("goals_input", "")
        goals_data = self.parse_goals(
            goals_input,
            (
                self.request.user.goals.summary
                if hasattr(self.request.user, "goals")
                else ""
            ),
        )

        goals_data["user"] = request.user.user_id

        serializer = self.get_serializer(data=goals_data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            logger.debug(
                f"{self.__class__.__name__}.{self.create.__name__}: User goals created successfully."
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.debug(
            f"{self.__class__.__name__}.{self.create.__name__}: User goals creation failed with errors: {serializer.errors}."
        )
        return Response(
            {
                "message": "User goals creation failed due to invalid data.",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def update(self, request, *args, **kwargs):
        logger.debug(
            f"{self.__class__.__name__}.{self.update.__name__}: Updating user goals."
        )
        partial = kwargs.pop("partial", False)
        try:
            instance = UserGoals.objects.get(user=request.user)
        except UserGoals.DoesNotExist:
            return Response(
                {"message": "User goals not found."}, status=status.HTTP_404_NOT_FOUND
            )

        goals_input = request.data.get("goals_input", "")
        goals_data = self.parse_goals(goals_input, instance.summary)

        serializer = self.get_serializer(instance, data=goals_data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(
                f"{self.__class__.__name__}.{self.update.__name__}: User goals updated successfully."
            )
            return Response(serializer.data)
        logger.debug(
            f"{self.__class__.__name__}.{self.update.__name__}: User goals update failed with errors: {serializer.errors}."
        )
        return Response(
            {
                "message": "User goals update failed due to invalid data.",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=False, methods=["delete"])
    def delete_goals(self, request):
        logger.debug(
            f"{self.__class__.__name__}.{self.delete_goals.__name__}: Deleting user goals."
        )
        UserGoals.objects.filter(user=self.request.user).delete()
        return Response(
            {"message": "User goals deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )

    def parse_goals(self, input_text, current_summary):
        logger.debug(
            f"{self.__class__.__name__}.{self.parse_goals.__name__}: Parsing goals input."
        )
        # Simulating a call to an LLM to parse natural language input
        new_summary = (
            current_summary + " " + input_text if current_summary else input_text
        )
        return {
            "summary": new_summary,
            "fat_goal": 42,
            "carb_goal": 42,
            "protein_goal": 42,
            "calorie_goal": 42,
            "weight_goal": 42,
        }
