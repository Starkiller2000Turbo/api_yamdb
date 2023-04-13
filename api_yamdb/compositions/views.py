from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models Reviews, Comments, Works,

from .permissions import (IsAuthorOrModeratorOrAdminOrReadOnly, )
from .serializers import (ReviewsSerializer, CommentsSerializer, )


class ReviewsViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов."""
    serializer_class = ReviewsSerializer
    permission_classes = (IsAuthorOrModeratorOrAdminOrReadOnly, )

    def get_works(self):
        return get_object_or_404(Works, id=self.kwargs.get('works_id'))

    def get_queryset(self):
        return self.get_works().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, works=self.get_title())
    


class CommentsViewSe(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""
    serializer_class = CommentsSerializer
    permission_classes = (IsAuthorOrModeratorOrAdminOrReadOnly, )

    def get_reviews(self):
        return get_object_or_404(Reviews, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_reviews().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())