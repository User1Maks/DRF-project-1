from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status

from education.models import Course, Lesson
from education.paginators import EducationPaginator
from education.permissions import IsOwner
from education.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModer


class CourseViewSet(viewsets.ModelViewSet):
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
            self.permission_classes = (IsOwner | ~IsModer, )
        return super().get_permissions()


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = EducationPaginator


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated,)

    def perform_create(self, serializer):
        """Метод для автоматического добавления преподавателя урока"""
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner | ~IsModer)
