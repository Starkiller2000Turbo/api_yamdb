import datetime

from django.core.validators import MaxValueValidator
from django.db import models


class Category(models.Model):
    """Модель категории."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

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

    class Meta:
        ordering = ['name']

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
        through='GenreTitle',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
    )

    class Meta:
        ordering = ['id']
        default_related_name = 'titles'

    def __str__(self) -> str:
        """Задание текстового представления произведения.

        Returns:
            Поле name данного произведения
        """
        return self.name


class GenreTitle(models.Model):
    """Модель связи произведения и жанра"""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='title_to_genre',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genre_to_title',
    )

    def __str__(self) -> str:
        """Задание текстового представления произведения.

        Returns:
            Поле name данного произведения
        """
        return f'{self.title.name} is {self.genre.name}'
