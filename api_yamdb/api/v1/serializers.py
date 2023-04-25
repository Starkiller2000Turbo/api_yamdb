from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер модели пользователя"""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class TokenSerializer(serializers.Serializer):
    """Сериалайзер для получения токена"""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class SignUpSerializer(serializers.Serializer):
    """Сериалайзер для создания нового пользователя"""

    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[RegexValidator(r'^[\w.@+-]+\Z')],
    )
    email = serializers.EmailField(max_length=254, required=True)

    def validate_username(self, username):
        if username.lower() == 'me':
            raise serializers.ValidationError(
                'Нельзя зарегистрировать имя пользователя "me"',
            )
        return username

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        user = User.objects.filter(username=username).first()
        if user:
            if user.email != email:
                raise serializers.ValidationError(
                    'Пользователь с таким именем уже зарегистрирован',
                )
        user = User.objects.filter(email=email).first()
        if user:
            if user.username != username:
                raise serializers.ValidationError(
                    'Пользователь с такой почтой уже зарегистрирован',
                )
        return data

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        user, created = User.objects.get_or_create(
            username=username,
            email=email,
        )
        return user


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
        }


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
        }


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(
        source='reviews__score__avg',
        read_only=True,
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    def validate(self, data):
        request = self.context.get('request')

        if request.method == 'POST':
            title_id = self.context['view'].kwargs.get('title_id')
            title = get_object_or_404(Title, pk=title_id)
            if Review.objects.filter(
                author=request.user,
                title=title,
            ).exists():
                raise serializers.ValidationError('Отзыв уже существует.')
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(slug_field='text', read_only=True)

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        fields = ('id', 'text', 'pub_date', 'author', 'review')
        model = Comment
