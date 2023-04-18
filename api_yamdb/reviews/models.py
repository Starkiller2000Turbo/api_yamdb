from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from compositions.models import Title
from users.models import User


class Review(models.Model):
    """Отзыв на произведение + рейтинг"""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='title',
        related_name='reviews',
    )
    text = models.CharField(max_length=1000)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='autor',
        related_name='reviews',
    )
    score = models.IntegerField(
        verbose_name='ratings',
        validators=(MinValueValidator(1), MaxValueValidator(10)),
    )
    pub_date = models.DateTimeField(
        verbose_name='date_publication',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Reviews'
        unique_together = (
            'author',
            'title',
        )
        ordering = ['-pub_date']

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Коментарий на отзыв"""

    text = models.CharField(max_length=1000)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        verbose_name='date_publication',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Comments'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text
