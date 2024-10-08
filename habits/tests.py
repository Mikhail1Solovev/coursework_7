import os
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
from dotenv import load_dotenv
from habits.models import Habit
from habits.tasks import send_reminder

User = get_user_model()

class HabitAPITestCase(APITestCase):
    def setUp(self):
        # Создание пользователя для тестов
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.habit_url = reverse('habit-list')

    def test_create_habit(self):
        # Тестирование создания привычки
        data = {
            'user': self.user.id,
            'action': 'Read a book',
            'place': 'Home',
            'time': '18:00:00',
            'execution_time': 2
        }
        response = self.client.post(self.habit_url, data)
        if response.status_code == 400:
            print("Ошибка создания привычки:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['action'], 'Read a book')

    def test_update_habit(self):
        # Тестирование обновления привычки
        habit = Habit.objects.create(user=self.user, action='Read a book', place='Home', time='18:00:00', execution_time=2)
        update_url = reverse('habit-detail', args=[habit.id])
        data = {
            'user': self.user.id,
            'action': 'Read two books',
            'place': 'Home',
            'time': '19:00:00',
            'execution_time': 3
        }
        response = self.client.put(update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], 'Read two books')

    def test_delete_habit(self):
        # Тестирование удаления привычки
        habit = Habit.objects.create(user=self.user, action='Read a book', place='Home', time='18:00:00', execution_time=2)
        delete_url = reverse('habit-detail', args=[habit.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(id=habit.id).exists())

    @patch('celery.app.task.Task.apply_async')
    def test_send_reminder_task(self, mock_apply_async):
        # Тестирование отправки отложенного напоминания через Celery
        send_reminder(user_id=self.user.id, message='Time to read a book!')
        mock_apply_async.assert_called_once()
        args, kwargs = mock_apply_async.call_args
        self.assertIn('eta', kwargs)
