"""
URL configuration for blogproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,

)
from blog.views import MyObtainTokenPairView, RegisterView
from blog.views import UserViewSet, PostViewSet
router = DefaultRouter()


# Create your views here.
# | HTTP Method | URL            | Action              |
#| ----------- | -------------- | ------------------- |
#| GET         | `/users/`      | list all users      |
#| POST        | `/users/`      | create a user       |
#| GET         | `/users/<id>/` | get user by ID      |
#| PUT         | `/users/<id>/` | update user         |
#| PATCH       | `/users/<id>/` | partial update user |
#| DELETE      | `/users/<id>/` | delete user         |
router.register(r'users', UserViewSet)


# | Method | URL               | Description             |
# | ------ | ----------------- | ----------------------- |
# | GET    | `/api/posts/`     | List all your posts     |
# | POST   | `/api/posts/`     | Create a new post       |
# | GET    | `/api/posts/:id/` | Retrieve a single post  |
# | PUT    | `/api/posts/:id/` | Update a post (you own) |
# | DELETE | `/api/posts/:id/` | Delete a post (you own) |

router.register(r'api/posts', PostViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='auth_register'),
    path('', include(router.urls)),
]
