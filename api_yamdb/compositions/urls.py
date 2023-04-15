from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (ReviewViewSet, CommentViewSet,)

app_name = 'compositions'

router = DefaultRouter()

router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
