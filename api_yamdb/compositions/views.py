from django.core.exceptions import SuspiciousOperation
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets

from compositions.models import Category, Genre, Review, Title
from compositions.permissions import (
    IsAdminUserOrReadOnly,
    IsAuthorOrModeratorOrAdminOrReadOnly,
)
from compositions.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет, обрабатывающий запросы к произведениям."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('genre__slug', 'name', 'year', 'category__slug')

    def perform_create(self, serializer: TitleSerializer) -> None:
        """Автоматическое добавление пользователля.

        Args:
            serializer: сериализатор, содержащий информацию о посте.
        """
        if (
            not Genre.objects.filter(
                slug=self.request.data.get('genre', None),
            )
        ) or (
            not Category.objects.filter(
                slug=self.request.data.get('category', None),
            )
        ):
            raise SuspiciousOperation()
        genre = Genre.objects.get(
            slug=self.request.data.get('genre', None),
        )
        category = Category.objects.get(
            slug=self.request.data.get('category', None),
        )
        try:
            serializer.save(genre=genre, category=category)
        except IntegrityError:
            raise SuspiciousOperation()


class GenreList(generics.ListCreateAPIView):
    """Вьюсет, обрабатывающий запросы к списку жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreDetail(generics.RetrieveUpdateDestroyAPIView):
    """Вьюсет, обрабатывающий запросы к конкретному жанру."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly,)

    def get_object(self) -> Genre:
        slug = self.kwargs.get('slug')
        return get_object_or_404(Genre, slug=slug)


class CategoryList(generics.ListCreateAPIView):
    """Вьюсет, обрабатывающий запросы к списку категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    """Вьюсет, обрабатывающий запросы к конкретной категории."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)

    def get_object(self) -> Category:
        slug = self.kwargs.get('slug')
        return get_object_or_404(Category, slug=slug)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModeratorOrAdminOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSe(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModeratorOrAdminOrReadOnly,)

    def get_reviews(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_reviews().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
