import logging

from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Meal, FoodComponent, HistoricalMeal
from .models import UserGoals
from .serializers import UserGoalsSerializer
from .serializers import (
    UserSerializer,
    MealSerializer,
    FoodComponentSerializer,
    HistoricalMealSerializer,
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
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        logger.debug(f"User registered with username: {user.username}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        logger.debug(f"Registration failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or password is None:
        return Response(
            {"error": "Please provide both username and password."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    logger.debug(f"Attempting to authenticate user: {username}")
    user = authenticate(username=username, password=password)
    if user:
        logger.debug(f"User authenticated: {username}")
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )

    logger.debug(f"Invalid credentials for user: {username}")
    return Response(
        {"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED
    )


class MealViewSet(viewsets.ModelViewSet):
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Meal.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.user_id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.debug(f"Meal creation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["put"])
    def edit_meal(self, request, pk=None):
        meal = self.get_object()
        serializer = MealSerializer(meal, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            logger.debug(f"Meal update failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FoodComponentViewSet(viewsets.ModelViewSet):
    serializer_class = FoodComponentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FoodComponent.objects.filter(meal__user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.debug(f"Food component creation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["put"])
    def edit_food_component(self, request, pk=None):
        food_component = self.get_object()
        serializer = FoodComponentSerializer(
            food_component, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            logger.debug(f"Food component update failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HistoricalMealViewSet(viewsets.ModelViewSet):
    serializer_class = HistoricalMealSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HistoricalMeal.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.user_id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.debug(f"Historical meal creation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def add_historical_meal(self, request):
        return self.create(request)

    @action(detail=False, methods=["get"])
    def list_historical_meals(self, request):
        historical_meals = self.get_queryset()
        serializer = HistoricalMealSerializer(historical_meals, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["put"])
    def edit_historical_meal(self, request, pk=None):
        historical_meal = self.get_object()
        serializer = HistoricalMealSerializer(
            historical_meal, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            logger.debug(f"Historical meal update failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserGoalsViewSet(viewsets.ModelViewSet):
    serializer_class = UserGoalsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure only the authenticated user's goals are returned
        return UserGoals.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Parse the goals using a placeholder method
        goals_data = self.parse_goals(request.data.get("goals_input", ""))
        # Attach the current user to the parsed goals data
        goals_data['user'] = request.user.user_id

        # Serialize the data and save it
        serializer = self.get_serializer(data=goals_data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Ensure user is saved
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def parse_goals(self, input_text):
        # Placeholder function to mimic goal parsing
        return {
            "fat_goal": 42,
            "carb_goal": 42,
            "protein_goal": 42,
            "calorie_goal": 42,
            "weight_goal": 42
        }

    def update(self, request, *args, **kwargs):
        # Use update for changing existing goals
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        goals_data = self.parse_goals(request.data.get("goals_input", ""))
        serializer = self.get_serializer(instance, data=goals_data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

