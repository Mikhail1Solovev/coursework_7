from rest_framework import serializers
from .models import Course, Lesson, Habit
from users.models import CustomUser

# Сериализатор для модели пользователя
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'date_of_birth', 'phone_number', 'address']

# Сериализатор для модели курса
class CourseSerializer(serializers.ModelSerializer):
    owner = CustomUserSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'owner', 'is_public']

# Сериализатор для модели урока
class LessonSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()

    class Meta:
        model = Lesson
        fields = ['id', 'course', 'title', 'content', 'video_link', 'duration_minutes']

# Сериализатор для модели привычки
class HabitSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Habit
        fields = ['id', 'user', 'action', 'place', 'time', 'reward', 'linked_habit', 'is_pleasant', 'frequency', 'estimated_time', 'is_public']