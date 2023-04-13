from rest_framework import serializers

from compositions.models import Category, Genre, Title


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(),
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',  queryset=Category.objects.all(),
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )
        model = Title


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'slug',
        )
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'slug',
        )
        model = Category
