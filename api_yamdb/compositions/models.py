import datetime

from django.core.validators import MaxValueValidator
from django.db import models


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
