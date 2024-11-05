from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from education.models import Course, Lesson
from education.permissions import IsOwner
from education.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def create(self, request, *args, **kwargs):
        """Метод для автоматического добавления автора курса"""
        # Устанавливаем текущего пользователя как владельца курса
        request.data['owner'] = request.user.id

        # Создаем и сохраняем курс с обновленными данными
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Проверка валидности данных
        self.perform_create(serializer)  # Сохраняем объект

        return Response(serializer.data)  # Возвращаем данные о
        # созданном объекте

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
