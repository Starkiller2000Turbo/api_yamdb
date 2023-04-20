from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    UserViewSet,
    get_token,
    signup,
)

app_name = '%(app_label)s'

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='user')
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', signup, name='register_user'),
    path('auth/token/', get_token, name='token'),
]
