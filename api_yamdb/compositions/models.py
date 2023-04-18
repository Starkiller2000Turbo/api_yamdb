import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Category(models.Model):
    """Модель категории."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self) -> str:
        """Задание текстового представления категории.

        Returns:
            Поле name данной категории
        """
        return self.name


class Genre(models.Model):
    """Модель жанра."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self) -> str:
        """Задание текстового представления жанра.

        Returns:
            Поле name данного жанра
        """
        return self.name


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(max_length=256)
    year = models.IntegerField(
        validators=[
            MaxValueValidator(limit_value=datetime.datetime.now().year),
        ],
    )
    description = models.TextField(null=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        null=False,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='titles',
        null=False,
    )

    def __str__(self) -> str:
        """Задание текстового представления произведения.

        Returns:
            Поле name данного произведения
        """
        return self.name


class Review(models.Model):
    """Отзыв на произведение + рейтинг"""

    works = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='title',
        related_name='reviews',
    )
    text = models.CharField(max_length=1000)
    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='autor',
        related_name='reviews',
    )
    ratings = models.IntegerField(
        verbose_name='ratings',
        validators=(MinValueValidator(1), MaxValueValidator(10)),
    )

    class Meta:
        verbose_name = 'Reviews'

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Коментарий на отзыв"""

    text = models.CharField(max_length=1000)
    reviews = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='comments',
        related_name='reviews',
    )
    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='autor',
        related_name='comments',
    )
    pub_date = models.DateField(
        verbose_name='date_publication',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Comments'

    def __str__(self):
        return self.text
