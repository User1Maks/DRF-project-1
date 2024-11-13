from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from education.models import NULLABLE, Course, Lesson


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


class Payments(models.Model):
    """Модель платежей"""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='payments')
    payment_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               verbose_name='Оплаченный курс',
                               related_name='payments', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE,
                               **NULLABLE,
                               verbose_name='Оплаченный урок',
                               related_name='payments')
    payment_amount = models.PositiveIntegerField(
        verbose_name='Сумма оплаты',
        **NULLABLE,
        help_text='Введите сумму оплаты')
    payment_by_card = models.BooleanField(verbose_name='Оплата картой',
                                          default=False)
    cash_payment = models.BooleanField(verbose_name='Оплата наличными',
                                       default=False)
    session_id = models.CharField(
        max_length=255,
        **NULLABLE,
        verbose_name='Id сессии',
        help_text='Введите id сессии для оплаты'
    )
    link = models.URLField(
        max_length=400,
        **NULLABLE,
        verbose_name='Ссылка на оплату',
        help_text='Укажите ссылку на оплату'
    )

    def __str__(self):
        return f'{self.payment_date} - {self.payment_amount}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'


class Subscriptions(models.Model):
    """Модель подписки на обновление курса"""
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='subscriptions')
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               related_name='subscriptions')

    def __str__(self):
        return f'{self.user} подписка на {self.course}.'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
