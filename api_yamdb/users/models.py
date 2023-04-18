from django.db import models
<<<<<<< HEAD
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    """Модель пользователя"""
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLES = (
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[RegexValidator(r'^[\w.@+-]+\Z')]
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
    )
    role = models.CharField(
        'Уровень доступа',
        max_length=20,
        default='user',
        choices=ROLES,
    )
    bio = models.TextField(
        'Информация по пользователе',
        null=True,
        blank=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=50,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=50,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='username_email'
            ),
            models.CheckConstraint(
                check=~models.Q(username='me'),
                name='not_me'
            )
        ]

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.ADMIN

    def __str__(self):
        return self.username
=======

# Create your models here.
>>>>>>> feature/Rewiews_comments_Raitings
