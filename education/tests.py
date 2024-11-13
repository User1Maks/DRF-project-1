from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from education.models import Course, Lesson
from users.models import Subscriptions, User


class CourseTestCase(APITestCase):
    """Тестирование функционала класса Course."""

    def setUp(self):
        # self.moderator_group = Group.objects.create(name='moders')
        # self.user_moderator = User.objects.create(email='moderator@sky.pro',
        #                                           is_staff=True)
        self.user = User.objects.create(email='user@sky.pro')
        # self.user_moderator.groups.add(self.moderator_group)

        self.course = Course.objects.create(
            name='Python разработчик',
            description='Создает сервисы на языке Python',
            owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name='DRF',
            description='django rest framework',
            owner=self.user,
            course=self.course
        )
        # авторизуем пользователя
        self.client.force_authenticate(user=self.user)

    def test_course_create(self):
        """Тест на создание курса"""
        url = reverse('education:course-list')
        data = {
            'name': 'Java-разработчик',
            'description': 'Создает сервисы для миллионов людей',
            'owner': self.user.id
        }
        response = self.client.post(url, data)

        # Проверяем пользователя
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_retrieve(self):
        """Тест на просмотр курса."""
        url = reverse('education:course-detail',
                      args=(self.course.id,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        # Проверка полей данных
        self.assertEqual(data.get('name'), self.course.name)
        self.assertEqual(data.get('id'), self.course.id)

        self.assertEqual(data['lessons'][0]['name'], self.lesson.name)

    def test_course_update(self):
        """Тест на обновление курса."""
        url = reverse('education:course-detail',
                      args=(self.course.pk,))
        data = {
            'name': 'Python developer'
        }
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(data.get('name'), 'Python developer')

    def test_course_delete(self):
        """Тест на удаление курса."""
        url = reverse('education:course-detail',
                      args=(self.course.pk,))

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Course.objects.all().count(), 0
        )

    def test_course_list(self):
        """Тест на вывод списка курсов с пагинацией."""
        url = reverse('education:course-list')
        response = self.client.get(url)
        data = response.json()

        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "number_of_lessons": 1,
                    "lessons": [
                        {
                            "id": self.lesson.pk,
                            "name": self.lesson.name,
                            "description": self.lesson.description,
                            "image": None,
                            "link_to_video": None,
                            "course": self.course.pk,
                            "owner": self.user.pk
                        }
                    ],
                    "is_subscribed": False,
                    "name": self.course.name,
                    "image": None,
                    "description": self.course.description,
                    "owner": self.user.pk
                }
            ]
        }

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )


class LessonTestCase(APITestCase):
    """Тестирование функционала класса Lesson."""

    def setUp(self):
        self.user = User.objects.create(email='user@sky.com')
        self.course = Course.objects.create(
            name='Test course name',
            description='Course description',
            owner=self.user)
        self.lesson = Lesson.objects.create(
            name='Test lesson name',
            description='Lesson description',
            owner=self.user,
            course=self.course
        )
        # авторизуем пользователя
        self.client.force_authenticate(user=self.user)

    def test_lesson_create(self):
        """Тест на создание урока"""
        url = reverse('education:lesson-create')
        data = {
            'name': 'Name 2',
            'description': 'Description 2',
            'link_to_video': 'https://www.youtube.com/watch',
            'course': self.course.pk,
            'owner': self.user.pk
        }
        response = self.client.post(url, data)

        # Проверка статуса ответа
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )

        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_retrieve(self):
        """Тест на просмотр урока"""
        url = reverse('education:lesson-get', args=(self.lesson.pk,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['name'], self.lesson.name)
        self.assertEqual(response.data['description'], self.lesson.description)
        self.assertEqual(response.data['link_to_video'],
                         self.lesson.link_to_video)
        self.assertEqual(response.data['course'], self.course.pk)
        self.assertEqual(response.data['owner'], self.user.pk)

    def test_lesson_update(self):
        """Тест на обновление урока"""
        url = reverse('education:lesson-update', args=(self.lesson.pk,))
        data = {
            'name': 'Первый урок'
        }
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), 'Первый урок')

    def test_lesson_delete(self):
        """Тест на удаление урока"""
        url = reverse('education:lesson-delete', args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        """Тест на вывод списка уроков с пагинацией."""

        # self.maxDiff = None  #  для более детального вывода расхождений

        url = reverse('education:course-list')
        response = self.client.get(url)
        data = response.json()

        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.course.id,
                    'image': None,
                    'description': self.course.description,
                    'name': self.course.name,
                    'is_subscribed': False,
                    'number_of_lessons': 1,
                    'lessons': [
                        {
                            'id': self.lesson.id,
                            'name': self.lesson.name,
                            'description': self.lesson.description,
                            'image': None,
                            'link_to_video': self.lesson.link_to_video,
                            'course': self.course.id,
                            'owner': self.user.id
                        }
                    ],
                    'owner': self.user.id
                }
            ]
        }

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(data, result)


class SubscriptionTestCase(APITestCase):
    """Тестирование функционала подписки."""

    def setUp(self):
        self.user = User.objects.create(email='user@sky.com')
        self.course = Course.objects.create(
            name='Test course name',
            description='Course description',
            owner=self.user)

        self.subscription = Subscriptions.objects.create(
            user=self.user,
            course=self.course,
            subscription=True
        )

        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        """Тест на создание подписки на курс."""
        url = reverse('users:subscription-list')
        data = {
            'user': self.user.id,
            'course': self.course.id,
            'subscription': True
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscriptions.objects.count(), 2)

    def test_subscription_update(self):
        """Тест на изменение подписки на курс."""
        url = reverse('users:subscription-detail', args=(self.subscription.pk,))
        data = {
            'subscription': False
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('subscription'), False)

    def test_subscription_delete(self):
        """Тест на удаление подписки на курс."""
        url = reverse('users:subscription-detail', args=(self.subscription.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subscriptions.objects.count(), 0)
