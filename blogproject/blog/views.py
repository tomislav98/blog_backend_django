from django.shortcuts import render
from rest_framework import viewsets
from .models import User, Post, Comment
from .serializers import UserSerializer, CommentSerializer, MyTokenObtainPairSerializer, PostSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import MultiPartParser, FormParser

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

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_pk']  # Or however you get post id from URL
        return Comment.objects.filter(post_id=post_id, status='PENDING').order_by('created_at')

    def perform_create(self, serializer):
        post_id = self.kwargs['post_pk']
        serializer.save(user=self.request.user, post_id=post_id)
