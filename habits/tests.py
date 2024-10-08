from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Course, Lesson, Habit
from users.models import CustomUser

# Тесты для модели курса
class CourseTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='Test Course', description='Course Description', owner=self.user, is_public=True)

    def test_create_course(self):
        data = {'title': 'New Course', 'description': 'New Course Description'}
        response = self.client.post(reverse('course-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)

    def test_get_course_list(self):
        response = self.client.get(reverse('course-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_course(self):
        data = {'title': 'Updated Course Title'}
        response = self.client.patch(reverse('course-detail', args=[self.course.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, 'Updated Course Title')

# Тесты для модели привычек
class HabitTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.habit = Habit.objects.create(user=self.user, action='Morning Run', place='Park', time='07:00:00', frequency=1, estimated_time=60)

    def test_create_habit(self):
        data = {'action': 'Evening Walk', 'place': 'Beach', 'time': '18:00:00', 'frequency': 1, 'estimated_time': 30}
        response = self.client.post(reverse('habit-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)

    def test_get_habit_list(self):
        response = self.client.get(reverse('habit-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_complete_habit(self):
        response = self.client.post(reverse('habit-complete', args=[self.habit.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertIsNotNone(self.habit.last_completed)