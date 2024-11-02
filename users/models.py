from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from education.models import Course, Lesson, NULLABLE


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
    payment_date = models.DateField(verbose_name='Дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE,
                                    verbose_name='Оплаченный курс',
                                    related_name='payments')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE,
                                    verbose_name='Оплаченный урок',
                                    related_name='payments')
    payment_amount = models.PositiveIntegerField(
        verbose_name='Сумма оплаты',
        help_text='Введите сумму оплаты')
    payment_by_card = models.BooleanField(verbose_name='Оплата картой',
                                          default=False)
    cash_payment = models.BooleanField(verbose_name='Оплата наличными',
                                       default=False)

    def __str__(self):
        return f'{self.payment_date} - {self.payment_amount}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
