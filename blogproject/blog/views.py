from rest_framework import viewsets
from .models import User, Post, Comment, Tag
from .serializers import UserSerializer, CommentSerializer, MyTokenObtainPairSerializer, PostSerializer, TagSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import MultiPartParser, FormParser
from .pagination import SmallResultsSetPagination
from rest_framework import viewsets, filters
from django.db.models import QuerySet
from rest_framework.request import Request


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
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']  # allow ordering by created_at field
    ordering = ['-created_at']  # default ordering newest first


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
            # Allow anyone to read (GET), but require auth for create/update/delete
            if self.action in ['list', 'retrieve']:
                return [AllowAny()]
            return [IsAuthenticated()]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CommentSerializer


    def get_queryset(self):
        post_id = self.kwargs['post_pk']  # Or however you get post id from URL
        return Comment.objects.filter(post_id=post_id, status='APPROVED').order_by('created_at')

    def perform_create(self, serializer):
        post_id = self.kwargs['post_pk']
        serializer.save(user=self.request.user, post_id=post_id)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]


    def get_comment_count(self, post_id):
        count = Comment.objects.filter(post_id=post_id, status='APPROVED').count()
        return count

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]  #
    pagination_class = SmallResultsSetPagination


class PostListByCategoryView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self) -> QuerySet[Post]:
        request = cast(Request, self.request)

        category_name = request.query_params.get('category')
        queryset = Post.objects.all()

        if category_name:
            queryset = queryset.filter(
                post_categories__category__name__iexact=category_name,
                status=Post.Status.PUBLISHED
            ).distinct()

        return queryset


class PostListByTagSlugView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        tag_slug = self.request.query_params.get('tag')
        queryset = Post.objects.all()

        if tag_slug:
            queryset = queryset.filter(
                post_tags__tag__slug=tag_slug,
                status=Post.Status.PUBLISHED
            ).distinct()

        return queryset
