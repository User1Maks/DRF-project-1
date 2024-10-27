from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """Модель пользователя"""
    username = None
    first_name = models.CharField(max_length=50, **NULLABLE, verbose_name='Имя')
    last_name = models.CharField(max_length=50, **NULLABLE,
                                 verbose_name='Фамилия')
    email = models.EmailField(unique=True, verbose_name='Email')
    avatar = models.ImageField(
        upload_to='users/avatars/',
        verbose_name='Аватар',
        **NULLABLE,
        help_text='Загрузите ваш аватар'
    )
    phone = PhoneNumberField(
        verbose_name='Телефон',
        **NULLABLE,
        help_text='Введите номер телефона'
    )
    city = models.CharField(
        max_length=100,
        verbose_name='Город',
        **NULLABLE,
        help_text='Введите город'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
