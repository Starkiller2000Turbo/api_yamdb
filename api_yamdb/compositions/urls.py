from django.urls import include, path
from rest_framework.routers import SimpleRouter

from compositions.views import (
    CategoryDetail,
    CategoryList,
    GenreDetail,
    GenreList,
    TitleViewSet,
)

app_name = '%(app_label)s'

router = SimpleRouter()
router.register('titles', TitleViewSet)

urlpatterns = [
    path('categories/', CategoryList.as_view()),
    path('categories/<slug:slug>/', CategoryDetail.as_view()),
    path('genres/', GenreList.as_view()),
    path('genres/<slug:slug>/', GenreDetail.as_view()),
    path('', include(router.urls)),
]
