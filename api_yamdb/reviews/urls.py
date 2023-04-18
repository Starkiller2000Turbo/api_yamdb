from django.urls import include, path
from rest_framework.routers import SimpleRouter

from reviews.views import CommentViewSet, ReviewViewSet

app_name = '%(app_label)s'

router = SimpleRouter()
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
    path('', include(router.urls)),
]
