from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Reviews(models.Model):
    """Отзыв на произведение + рейтинг"""
    works = models.ForeignKey(Title, on_delete=models.CASCADE,
                              verbose_name='title', related_name='reviews')
    text = models.CharField(max_length=1000)
    autor = models.ForeignKey(User, on_delete=models.CASCADE,
                              verbose_name='autor', related_name='reviews')
    ratings = models.IntegerField(verbose_name='ratings',
                                  validators=(MinValueValidator(1),
                                              MaxValueValidator(10)))

    class Meta:
        verbose_name = 'Reviews'

    def __str__(self):
        return self.text


class Comments(models.Model):
    """Коментарий на отзыв"""
    text = models.CharField(max_length=1000)
    reviews = models.ForeignKey(Reviews, on_delete=models.CASCADE,
                                verbose_name='comments',
                                related_name='reviews')
    autor = models.ForeignKey(User, on_delete=models.CASCADE,
                              verbose_name='autor', related_name='comments')
    pub_date = models.DateField(verbose_name='date_publication',
                                auto_now_add=True)

    class Meta:
        verbose_name = 'Comments'

    def __str__(self):
        return self.text
