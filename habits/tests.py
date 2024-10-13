from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
from habits.models import UserHabit
from habits.tasks import send_reminder
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class HabitAPITestCase(APITestCase):
    def setUp(self):
        # Создание пользователя для тестов (email обязателен)
        self.user = User.objects.create_user(
            email='testuser@example.com', password='password123')
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        self.habit_url = reverse('habit-list')

    def test_create_habit(self):
        # Тестирование создания привычки
        data = {
            'user': self.user.id,
            'action': 'Read a book',
            'periodicity': 2,
            'execution_time': 120
        }
        response = self.client.post(self.habit_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['action'], 'Read a book')

    def test_update_habit(self):
        # Тестирование обновления привычки
        habit = UserHabit.objects.create(
            user=self.user,
            action='Read a book',
            periodicity=2,
            execution_time=120)
        update_url = reverse('habit-detail', args=[habit.id])
        data = {
            'user': self.user.id,
            'action': 'Read two books',
            'periodicity': 3,
            'execution_time': 100
        }
        response = self.client.put(update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], 'Read two books')

    def test_delete_habit(self):
        # Тестирование удаления привычки
        habit = UserHabit.objects.create(
            user=self.user,
            action='Read a book',
            periodicity=2,
            execution_time=120)
        delete_url = reverse('habit-detail', args=[habit.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(UserHabit.objects.filter(id=habit.id).exists())


class HabitModelTestCase(APITestCase):
    def setUp(self):
        # Создание пользователя для теста
        self.user = User.objects.create_user(
            email='testuser@example.com', password='password123')

    def test_create_habit(self):
        # Тест создания привычки
        habit = UserHabit.objects.create(
            user=self.user,
            action='Read',
            periodicity=5,
            execution_time=100)
        self.assertEqual(habit.action, 'Read')
        self.assertEqual(habit.execution_time, 100)

    def test_habit_str(self):
        # Тест строкового представления привычки
        habit = UserHabit.objects.create(
            user=self.user,
            action='Read',
            periodicity=5,
            execution_time=100)
        # Исправление для строки
        self.assertEqual(str(habit), 'Read (testuser@example.com)')


class TaskTestCase(APITestCase):
    @patch('telegram.Bot.send_message')
    def test_send_reminder(self, mock_send_message):
        # Тест задачи отправки напоминания
        send_reminder(chat_id=12345, message='Test message')
        mock_send_message.assert_called_once_with(
            chat_id=12345, text='Test message')
