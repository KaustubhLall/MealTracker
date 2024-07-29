from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Meal, FoodComponent, HistoricalMeal
from .serializers import (
    UserSerializer,
    MealSerializer,
    FoodComponentSerializer,
    HistoricalMealSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


@api_view(["POST"])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
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

    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )

    return Response(
        {"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED
    )


class MealViewSet(viewsets.ModelViewSet):
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Meal.objects.filter(user=self.request.user)

    @action(detail=True, methods=["put"])
    def edit_meal(self, request, pk=None):
        meal = self.get_object()
        serializer = MealSerializer(meal, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FoodComponentViewSet(viewsets.ModelViewSet):
    serializer_class = FoodComponentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FoodComponent.objects.filter(meal__user=self.request.user)

    @action(detail=True, methods=["put"])
    def edit_food_component(self, request, pk=None):
        food_component = self.get_object()
        serializer = FoodComponentSerializer(
            food_component, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HistoricalMealViewSet(viewsets.ModelViewSet):
    serializer_class = HistoricalMealSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HistoricalMeal.objects.filter(user=self.request.user)

    @action(detail=False, methods=["post"])
    def add_historical_meal(self, request):
        serializer = HistoricalMealSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
