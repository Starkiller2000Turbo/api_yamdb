from django.conf import settings
from django.core.mail import send_mail


def send_confirmation_code(user, code):
    """Функция отправки кода подтверждения на почту"""
    send_mail(message=f' Ваш код подтверждения: {code}',
              subject='Добро пожаловать на проект Yatube',
              recipient_list=[user.email,],
              from_email=settings.DEFAULT_EMAIL)
