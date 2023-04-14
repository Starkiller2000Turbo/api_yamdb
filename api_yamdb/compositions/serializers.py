from rest_framework import serializers

from compositions.models import Category, Genre, Title


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name',
            'slug',
        )
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name',
            'slug',
        )
        model = Category


class GenreListingField(serializers.RelatedField):

    def to_representation(self, value):
        return value.slug


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreListingField(queryset=Genre.objects.all, many=True)
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
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
