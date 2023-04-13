from rest_framework import serializers
from django.shortcuts import get_object_or_404

from .models Comments, Reviews, Title,


class ReviewsSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""
    works = serializers.SlugRelatedField(
        slug_field='name', read_only=True)
    
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    
    ratings = serializers.IntegerField(min_value=1, max_value=10)

    def validate(self, data):
        request = self.context.get('request')

        if request.method == 'POST':
            title_id = self.context['view'].kwargs.get('title_id')
            title = get_object_or_404(Title, pk=title_id)
            if Review.objects.filter(author=request.user, title=title).exists():
                raise ValidationError('Отзыв уже существует.')
        return data
        

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Reviews


class CommentsSerializer(serializers.ModelSerializer):
    """"Сериализатор для комментариев на отзывы."""
    review = serializers.SlugRelatedField(
        slug_field='text', read_only=True)

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'pub_date', 'author', 'review')
        model = Comments