from datetime import datetime, timedelta

from celery import shared_task
from pytz import timezone

from config import settings
from users.models import User


@shared_task
def last_login_check():
    """
    Проверяет дату последнего входа пользователя. Если пользователь не заходил
    более месяца, то блокирует его.
    """
    # выбираем активных пользователй
    users = User.objects.filter(is_active=True)
    time_zone = timezone(settings.TIME_ZONE)
    current_date = datetime.now(time_zone)

    for user in users:
        if user.last_login and user.last_login + timedelta(
                days=30) < current_date:
            user.is_active = False
            user.save()
