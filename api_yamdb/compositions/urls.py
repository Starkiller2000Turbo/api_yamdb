from django.urls import include, path
from rest_framework.routers import DefaultRouter

from compositions.views import CategoryViewSet, GenreViewSet, TitleViewSet

app_name = '%(app_label)s'

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
