from rest_framework import serializers

from education.models import Course, Lesson
from education.validators import validate_link_to_video
from users.models import User, Subscriptions


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [validate_link_to_video]


class CourseSerializer(serializers.ModelSerializer):
    number_of_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_number_of_lessons(self, course):
        """Метод для возвращения количества уроков """
        count_lessons = Lesson.objects.filter(course=course).count()
        return count_lessons

    def get_is_subscribed(self, course):
        """Метод для возвращения подписок пользователя"""
        user = self.context.get('request').user

        #  Проверяем, аутентифицирован ли пользователь
        if user.is_authenticated:
            sub = Subscriptions.objects.filter(
                user=user,
                course=course,
                subscription=True  # Проверяем, что подписка активна
            ).exists()
            return sub
        return False   # Если пользователь не аутентифицирован, возвращаем False


