from django.db import models

from compositions.validators import validate_year


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
