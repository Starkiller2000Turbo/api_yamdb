import django_filters
from django.db.models import Avg
from django_filters import rest_framework
from rest_framework import filters, mixins, viewsets

from compositions.models import Category, Genre, Title
from compositions.permissions import IsAdminUserOrReadOnly
from compositions.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleSerializer,
)


class TitlesFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name='category__slug',
    )
    genre = django_filters.CharFilter(
        field_name='genre__slug',
    )

    class Meta:
        model = Title
        fields = ['name', 'year', 'genre', 'category']


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет, обрабатывающий запросы к произведениям."""

    queryset = (
        Title.objects.all()
        .annotate(
            Avg('reviews__score'),
        )
        .order_by('name')
    )
    serializer_class = TitleSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in (
            'retrieve',
            'list',
        ):
            return TitleReadSerializer
        return TitleSerializer


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
