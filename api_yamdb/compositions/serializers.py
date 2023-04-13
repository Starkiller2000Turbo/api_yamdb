from rest_framework import serializers
from django.shortcuts import get_object_or_404

from .models Comments, Reviews, Works,


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
            works_id = self.context['view'].kwargs.get('works_id')
            works = get_object_or_404(Works, pk=works_id)
            if Review.objects.filter(author=request.user, works=works).exists():
                raise ValidationError('Отзыв уже существует.')
        return data
        

    class Meta:
        fields = '__all__'
        model = Reviews


class CommentsSerializer(serializers.ModelSerializer):
    """"Сериализатор для комментариев на отзывы."""
    review = serializers.SlugRelatedField(
        slug_field='text', read_only=True)

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comments