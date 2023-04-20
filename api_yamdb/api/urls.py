from django.apps import apps
from django.urls import include, path

urlpatterns = [
    path('v1/', include('api.v1.urls')),
    path(
        'v1/',
        include('reviews.urls', namespace=apps.get_app_config('reviews').name),
    ),
]
