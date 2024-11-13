from rest_framework.serializers import ModelSerializer

from users.models import Payments, Subscriptions, User


class PaymentsSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class UserSerializer(ModelSerializer):
    payments = PaymentsSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'city', 'payments',)


class SubscriptionsSerializer(ModelSerializer):

    class Meta:
        model = Subscriptions
        fields = '__all__'
