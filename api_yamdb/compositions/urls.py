from django.urls import include, path
from rest_framework.routers import SimpleRouter

from compositions.views import (
    CategoryDetail,
    CategoryList,
    CommentViewSet,
    GenreDetail,
    GenreList,
    ReviewViewSet,
    TitleViewSet,
)

app_name = '%(app_label)s'

router = SimpleRouter()
router.register('titles', TitleViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews',
)


urlpatterns = [
    path('categories/', CategoryList.as_view()),
    path('categories/<slug:slug>/', CategoryDetail.as_view()),
    path('genres/', GenreList.as_view()),
    path('genres/<slug:slug>/', GenreDetail.as_view()),
    path('', include(router.urls)),
    path('v1/', include(router.urls)),
    path('v1/auth/', include('users.urls')),
]
