from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import UserViewSet, PaymentsViewSet

app_name = UsersConfig.name

router = SimpleRouter()
router.register(r'list', UserViewSet, basename='users')
router.register(r'payments', PaymentsViewSet, basename='payments')

urlpatterns = router.urls
