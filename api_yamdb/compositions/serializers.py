from rest_framework import serializers

from compositions.models import Category, Genre, Title


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name',
            'slug',
        )
        model = Genre
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
        }


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name',
            'slug',
        )
        model = Category
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
