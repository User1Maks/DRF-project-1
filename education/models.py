from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название курса',
                            help_text='Введите название курса')
    image = models.ImageField(
        upload_to='course/images/',
        verbose_name='Превью (картинка) курса',
        **NULLABLE,
        help_text='Загрузите превью курса'
    )
    description = models.TextField(**NULLABLE, verbose_name='Описание курса',
                                   help_text='Введите описание курса')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              **NULLABLE,
                              verbose_name='Автор курса',
                              help_text='Укажите автора курса')

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена курса',
        help_text='Введите цену курса'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название урока',
                            help_text='Введите название урока')
    description = models.TextField(**NULLABLE, verbose_name='Описание урока',
                                   help_text='Введите описание урока')
    image = models.ImageField(
        upload_to='lesson/images/',
        verbose_name='Превью (картинка) урока',
        **NULLABLE,
        help_text='Загрузите превью урока'
    )
    link_to_video = models.TextField(**NULLABLE, verbose_name='Ссылка на видео',
                                     help_text='Вставьте ссылку на видео урока')
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Курс',
        help_text='Выберите курс',
        related_name='lessons'
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              **NULLABLE,
                              verbose_name='Преподаватель',
                              help_text='Укажите преподавателя урока')

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена урока',
        help_text='Введите цену урока'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
