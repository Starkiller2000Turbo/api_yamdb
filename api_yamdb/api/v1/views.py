from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import ModelViewSet

from .permissions import IsAdmin
from .serializers import SignUpSerializer, TokenSerializer, UserSerializer
from .utils import send_confirmation_code

User = get_user_model()


class UserViewSet(ModelViewSet):
    """Вьюсет для модели пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin,)
    http_method_names = ['get', 'post', 'patch', 'delete',]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=('get', 'patch',),
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        """Функция для получения информации о своем пользователе"""
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=HTTPStatus.OK)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)
            return Response(serializer.data, status=HTTPStatus.OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    "Функция регистрации новых пользователей и получения кода подтверждения"
    username = request.data.get('username')
    email = request.data.get('email')
    user = User.objects.filter(username=username, email=email)
    if user.exists():
        user = User.objects.get(username=username, email=email)
        code = default_token_generator.make_token(user)
        send_confirmation_code(user, code)
        return Response(request.data, status=HTTPStatus.OK)
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    serializer.save()
    user = User.objects.get(email=email, username=username)
    code = default_token_generator.make_token(user)
    send_confirmation_code(user, code)
    return Response(serializer.data, status=HTTPStatus.OK)


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
            {'access': str(token.access_token)}, status=HTTPStatus.OK
        )
    return Response(
        'Неверный код подтверждения', status=HTTPStatus.BAD_REQUEST)
