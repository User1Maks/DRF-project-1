from rest_framework import status, viewsets
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated

from education.models import Course, Lesson
from education.paginators import EducationPaginator
from education.permissions import IsOwner
from education.serializers import CourseSerializer, LessonSerializer
from education.tasks import send_email_info_update_course
from users.permissions import IsModer


class CourseViewSet(viewsets.ModelViewSet):
    """ ViewSet for course """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = EducationPaginator

    def create(self, request, *args, **kwargs):
        """Метод для автоматического добавления автора курса"""
        data = request.data.copy()
        data['owner'] = request.user.id
        return super().create(request, *args, **kwargs)

    def get_permissions(self):
        """Проверяем пользователя на права доступа и даем ему
        необходимый функционал"""
        if self.action == 'create':
            self.permission_classes = (~IsModer,)  # Пользователь не должен
            # быть модератором
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsModer | IsOwner,)  # или модератор
            # или владелец
        elif self.action == 'destroy':
            self.permission_classes = (IsOwner | ~IsModer,)
        return super().get_permissions()

    def perform_update(self, serializer):
        """Отправляет письмо пользователю при обновлении курса."""
        # Сохраняем объект курса
        instance = serializer.save()

        # Получаем объект курса
        course = instance

        # Отправляем email всем подписчикам курса
        send_email_info_update_course.delay(course.id)


class LessonListAPIView(ListAPIView):
    """ Lesson list endpoint """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = EducationPaginator


class LessonCreateAPIView(CreateAPIView):
    """ Lesson create endpoint """
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated,)

    def perform_create(self, serializer):
        """Метод для автоматического добавления преподавателя урока"""
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonRetrieveAPIView(RetrieveAPIView):
    """ Lesson retrieve endpoint """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonUpdateAPIView(UpdateAPIView):
    """ Lesson update endpoint """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyAPIView(DestroyAPIView):
    """ Lesson delete endpoint """
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner | ~IsModer)
