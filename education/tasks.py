from celery import shared_task
from django.core.mail import send_mail
from config import settings
from education.models import Course
from users.models import Subscriptions


@shared_task
def send_email_info_update_course(course_id):
    """
    Для отправки писем об обновлении курса только тем пользователям,
    которые на него подписаны.
    """

    # Получаем курс
    course = Course.objects.get(id=course_id)

    # Находим все подписки на этот курс
    subscriptions = Subscriptions.objects.filter(course=course)

    # # Получаем всех пользователей из подписок
    # user_emails = []

    for subscription in subscriptions:
        # user_emails.append(subscription.user.email)

        send_mail('Курс обновился',
                  f'''
                  Ваш курс {course.name} обновился. Мы стараемся ради
                  Вас. Желаем вам успехов в обучении и вдохновения на пути к
                  новым знаниям! ''',
                  settings.EMAIL_HOST_USER,
                  [subscription.user.email])
