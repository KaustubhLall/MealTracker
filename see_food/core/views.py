from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Meal, FoodComponent, HistoricalMeal
from .serializers import (
    UserSerializer,
    MealSerializer,
    FoodComponentSerializer,
    HistoricalMealSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


@api_view(["POST"])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(user.password)
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user = authenticate(username=email, password=password)  # Change to 'username' if using email as username
    if user:
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )
    return Response(
        {"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED
    )


class MealViewSet(viewsets.ModelViewSet):
    serializer_class = MealSerializer

    def get_queryset(self):
        return Meal.objects.filter(user=self.request.user)


class FoodComponentViewSet(viewsets.ModelViewSet):
    serializer_class = FoodComponentSerializer

    def get_queryset(self):
        return FoodComponent.objects.filter(user=self.request.user)


class HistoricalMealViewSet(viewsets.ModelViewSet):
    serializer_class = HistoricalMealSerializer

    def get_queryset(self):
        return HistoricalMeal.objects.filter(user=self.request.user)
