from django.urls import path
from rest_framework.routers import SimpleRouter

from education.apps import EducationConfig
from education.views import (CourseViewSet, LessonCreateAPIView,
                             LessonDestroyAPIView, LessonListAPIView,
                             LessonRetrieveAPIView, LessonUpdateAPIView)

app_name = EducationConfig.name

router = SimpleRouter()
router.register('', CourseViewSet)

urlpatterns = [
    path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lessons/create/', LessonCreateAPIView.as_view(),
         name='lesson-create'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(),
         name='lesson-get'),
    path('lessons/update/<int:pk>/', LessonUpdateAPIView.as_view(),
         name='lesson-update'),
    path('lessons/delete/<int:pk>/', LessonDestroyAPIView.as_view(),
         name='lesson-delete'),
] + router.urls
