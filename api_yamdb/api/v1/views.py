from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters import rest_framework
from rest_framework import filters, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from api.v1.filters import TitlesFilter
from api.v1.mixins import ListCreateDestroyViewSet
from api.v1.permissions import (
    IsAdmin,
    IsAdminUserOrReadOnly,
    IsAuthorOrModeratorOrAdminOrReadOnly,
)
from api.v1.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleReadSerializer,
    TitleSerializer,
    TokenSerializer,
    UserSerializer,
)
from api.v1.utils import send_confirmation_code
from reviews.models import Category, Genre, Review, Title

User = get_user_model()


class UserViewSet(ModelViewSet):
    """Вьюсет для модели пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdmin,
    )
    http_method_names = [
        'get',
        'post',
        'patch',
        'delete',
    ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=(
            'get',
            'patch',
        ),
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        """Функция для получения информации о своем пользователе"""
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=HTTPStatus.OK)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role)
        return Response(serializer.data, status=HTTPStatus.OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Функция регистрации пользователей и получения кода подтверждения"""
    username = request.data.get('username')
    email = request.data.get('email')
    user = User.objects.filter(username=username, email=email)
    if not user.exists():
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        serializer.save()
    user = User.objects.get(email=email, username=username)
    code = default_token_generator.make_token(user)
    send_confirmation_code(user, code)
    return Response(request.data, status=HTTPStatus.OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Функция для получения токена"""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        token = RefreshToken.for_user(user)
        return Response(
            {'access': str(token.access_token)},
            status=HTTPStatus.OK,
        )
    return Response(
        'Неверный код подтверждения',
        status=HTTPStatus.BAD_REQUEST,
    )


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


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModeratorOrAdminOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModeratorOrAdminOrReadOnly,)

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
