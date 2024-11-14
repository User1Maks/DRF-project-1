import stripe
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from education.models import Course
from education.serializers import CourseSerializer
from users.models import Payments, Subscriptions, User
from users.serializers import (PaymentsSerializer, SubscriptionsSerializer,
                               UserSerializer)
from users.services import (create_stripe_price, create_stripe_product,
                            create_stripe_sessions)


class UserListAPIView(generics.ListAPIView):
    """ User list endpoint """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """ User create endpoint """
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
    """ User retrieve endpoint """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserUpdateAPIView(generics.UpdateAPIView):
    """ User update endpoint """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDestroyAPIView(generics.DestroyAPIView):
    """ User delete endpoint """
    queryset = User.objects.all()


class PaymentsViewSet(viewsets.ModelViewSet):
    """ ViewSet for payments """
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('course', 'lesson', 'payment_by_card',
                        'cash_payment',)
    ordering_fields = ('payment_date',)

    def perform_create(self, serializer):
        """
         Создает продукт и цену, основываясь на данных платежа, а также
         запускается сессия оплаты и сохраняется ссылка на оплату.
        """

        payment = serializer.save(user=self.request.user)

        payment_amount = self.request.data.get('payment_amount')

        # создаем стоимость
        price = create_stripe_price(payment_amount)

        # Создаем сессию Stripe
        session_id, payment_link = create_stripe_sessions(price)

        # Сохраняем данные сессии и ссылки
        payment.session_id = session_id
        payment.link = payment_link
        payment.payment_amount = payment_amount
        payment.save()


class SubscriptionView(APIView):
    """ ViewSet for subscription """
    serializer_class = SubscriptionsSerializer

    def post(self, *args, **kwargs):
        """Метод для подписки и отписки пользователя от обновления курса."""
        # Получаем текущего пользователя
        user = self.request.user
        # Получаем id курса
        course_id = self.request.data.get('course')
        # Получаем объект курса из базы
        course_item = get_object_or_404(Course, pk=course_id)

        # Ищем подписку пользователя на данный курс
        subs_item = Subscriptions.objects.filter(user=user,
                                                 course=course_item).first()

        # Если подписка существует, удаляем ее
        if subs_item:
            subs_item.delete()
            message = 'подписка удалена'

        else:
            # Если подписка не существует, создаем ее
            Subscriptions.objects.create(user=user,
                                         course=course_item)
            message = 'подписка добавлена'

        return Response({'message': message}, status=status.HTTP_200_OK)
