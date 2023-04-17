from django.urls import include, path
from rest_framework import routers

from . import views

router_v1 = routers.DefaultRouter()

router_v1.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/signup/', views.signup, name='register_user'),
    path('auth/token/', views.get_token, name='token'),
]
