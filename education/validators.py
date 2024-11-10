from rest_framework.serializers import ValidationError


def validate_link_to_video(lesson: dict):
    """Метод для проверки, что ссылки видео с YouTube"""
    youtube = 'https://www.youtube.com/'

    link_to_video = lesson.get('link_to_video')

    if link_to_video and youtube not in link_to_video:
        raise ValidationError(
            'Ссылка должна ссылаться на ресурс youtube.com.')
