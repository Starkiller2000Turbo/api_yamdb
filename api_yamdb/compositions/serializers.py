from rest_framework import serializers

from compositions.models import Category, Genre, GenreTitle, Title


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


class GenreTitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all,
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Title.objects.all,
    )

    class Meta:
        fields = ('title','genre',)
        model = GenreTitle

    def to_representation(self, instance):
        return instance.genre.slug


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreTitleSerializer(
        source='title_to_genre',
        many=True,
        read_only=True,
    )
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


class TitleWithGenres(serializers.ModelSerializer):
    title = TitleSerializer()
    genretitle = GenreTitleSerializer(context={'title':title})

    class Meta:
        fields = (
            'title',
            'genretitle',
        )
