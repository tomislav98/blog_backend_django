from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from blog.views import (
    MyObtainTokenPairView, RegisterView,
    UserViewSet, PostViewSet, CommentViewSet, TagViewSet,
    PostListByTagSlugView, PostListByCategoryView
)

# Main router
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'tags', TagViewSet, basename='tag')

# Nested router for comments under posts
posts_router = routers.NestedSimpleRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', CommentViewSet, basename='post-comments')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Custom filtered views — ALL start with /api/
    path('api/posts/by-category/', PostListByCategoryView.as_view(), name='posts-by-category'),
    path('api/posts/by-tag/', PostListByTagSlugView.as_view(), name='post-list-by-tag-slug'),

    # API routers
    path('api/', include(router.urls)),
    path('api/', include(posts_router.urls)),

    # Auth endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/login/', MyObtainTokenPairView.as_view(), name='custom_token_obtain'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='custom_token_refresh'),
    path('api/register/', RegisterView.as_view(), name='auth_register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
