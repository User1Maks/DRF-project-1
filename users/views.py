from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from education.models import Course
from users.models import Payments, Subscriptions, User
from users.serializers import (PaymentsSerializer, SubscriptionsSerializer,
                               UserSerializer)


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    # Даем доступ для авторизации анонимным пользователям
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """Переопределяем метод создания пользователя, т.к. в модели User
        username = None"""
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()


class PaymentsViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_by_card',
                        'cash_payment',)
    ordering_fields = ('payment_date',)


class SubscriptionView(viewsets.ModelViewSet):
    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionsSerializer

    def post(self, *args, **kwargs):
        """Метод для подписки и отписки пользователя от обновления курса."""
        # Получаем текущего пользователя
        user = self.request.user
        # Получаем id курса
        course_id = self.request.data.get('course_id')
        # Получаем объект курса из базы
        course_item = get_object_or_404(Course, id=course_id)

        # Получаем объект подписки пользователя на данный курс
        subs_item = Subscriptions.objects.filter(user=user, course=course_item)

        # Если подписка у пользователя на этот курс есть - отключаем ее
        if subs_item.exists():
            subs_item.update(subscription=False)
            message = 'Подписаться'

        # Если подписки у пользователя на этот курс нет - активируем ее
        else:
            subs_item.update(subscription=True)
            message = 'Подписка активирована'

        return Response({'message': message})
