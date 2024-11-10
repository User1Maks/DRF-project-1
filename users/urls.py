from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView,
                                            TokenBlacklistView)

from users.apps import UsersConfig
from users.views import (PaymentsViewSet, UserCreateAPIView,
                         UserDestroyAPIView, UserListAPIView,
                         UserRetrieveAPIView, UserUpdateAPIView,
                         SubscriptionView)

app_name = UsersConfig.name

router = SimpleRouter()
router.register(r'payments', PaymentsViewSet, basename='payments')
router.register(r'subscription', SubscriptionView, basename='subscription')

urlpatterns = [
    # users
    path('register/', UserCreateAPIView.as_view(
        permission_classes=(AllowAny,)), name='register'),
    path('list/', UserListAPIView.as_view(), name='user-list'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
         name='login'),  # api/token/
    path('logout/', TokenBlacklistView.as_view(), name='user-logout'),
    path('token/refresh/', TokenRefreshView.as_view(
        permission_classes=(AllowAny,)), name='token-refresh'),
    path('profile/', UserRetrieveAPIView.as_view(), name='user-profile'),
    path('update_profile/', UserUpdateAPIView.as_view(), name='update-profile'),
    path('delete_profile/', UserDestroyAPIView.as_view(),
         name='delete-profile'),
] + router.urls

