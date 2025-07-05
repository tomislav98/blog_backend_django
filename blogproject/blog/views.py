from django.shortcuts import render
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer, MyTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.
# | HTTP Method | URL            | Action              |
#| ----------- | -------------- | ------------------- |
#| GET         | `/users/`      | list all users      |
#| POST        | `/users/`      | create a user       |
#| GET         | `/users/<id>/` | get user by ID      |
#| PUT         | `/users/<id>/` | update user         |
#| PATCH       | `/users/<id>/` | partial update user |
#| DELETE      | `/users/<id>/` | delete user         |
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]



class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    # Defines the set of objects this view works with
    queryset = User.objects.all()
    # Allows anyone (even unauthenticated users) to access this endpoint
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
