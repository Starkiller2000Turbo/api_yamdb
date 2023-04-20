from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validators import validate_year
from users.models import User


class Category(models.Model):
    """Модель категории."""

    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Слаг')

    class Meta:
        ordering = ['name']
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self) -> str:
        """Задание текстового представления категории.

        Returns:
            Поле name данной категории
        """
        return self.name


class Genre(models.Model):
    """Модель жанра."""

    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Слаг')

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        """Задание текстового представления жанра.

        Returns:
            Поле name данного жанра
        """
        return self.name


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(max_length=256, verbose_name='Название')
    year = models.IntegerField(
        validators=[validate_year],
        verbose_name='Год создания',
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание',
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )

    class Meta:
        ordering = ['id']
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

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
        verbose_name='Произведение',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр',
    )

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведения'

    def __str__(self) -> str:
        """Задание текстового представления произведения.

        Returns:
            Поле name данного произведения
        """
        return f'{self.title.name}, жанр - {self.genre.name}'


class Review(models.Model):
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
        error_messages={'validators': 'Оценка от 1 до 10!'},
    )
    pub_date = models.DateTimeField(
        verbose_name='date_publication',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Reviews'
        constraints = [
            models.UniqueConstraint(
                fields=(
                    'title',
                    'author',
                ),
                name='unique_review',
            ),
        ]
        ordering = ['-pub_date']

    def __str__(self):
        return self.text


class Comment(models.Model):
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
