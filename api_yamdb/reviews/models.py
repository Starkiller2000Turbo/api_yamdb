from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

User = get_user_model()


class Category(models.Model):
    """Модель категории."""

    name = models.CharField(
        'Название категории',
        max_length=256,
    )
    slug = models.SlugField(
        'Slug категории',
        unique=True,
        max_length=50,
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра."""

    name = models.CharField(
        'Название жанра',
        max_length=256,
    )
    slug = models.SlugField(
        'Slug жанра',
        unique=True,
        max_length=50,
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        'Название произведения',
        max_length=50,
    )
    year = models.IntegerField(
        'Год выпуска',
    )
    description = models.TextField(
        'Описание',
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        verbose_name='Slug жанра',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Slug категории',
    )

    class Meta:
        ordering = ('name',)
        default_related_name = 'title'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    """Связь произведение-жанр."""

    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)


class Review(models.Model):
    """Модель отзывов."""

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField(max_length=1000, verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='username пользователя',
    )
    score = models.SmallIntegerField(
        validators=[
            MinValueValidator(1, 'минимальная оценка 1'),
            MaxValueValidator(10, 'максимальная оценка 10'),
        ],
        verbose_name='Оценка',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации отзыва',
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=['title', 'author'], name='title_one_review'
            ),
        )

    def __str__(self):
        return self.author, self.text, self.score


class Comment(models.Model):
    """Модель комментариев."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='username автора комментария',
    )
    pub_date = models.DateTimeField(
        default=timezone.now, verbose_name='Дата публикации комментария'
    )

    class Meta:
        ordering = ('review', 'author')

    def __str__(self):
        return self.author, self.text
