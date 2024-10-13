from rest_framework import serializers
from .models import UserHabit


class UserHabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserHabit
        fields = '__all__'

    def validate(self, data):
        # Проверка времени выполнения
        if data.get('execution_time', 0) > 120:
            raise serializers.ValidationError("Время выполнения привычки не может превышать 120 секунд.")

        # Проверка одновременного указания вознаграждения и связанной привычки
        if data.get('reward') and data.get('linked_habit'):
            raise serializers.ValidationError("Нельзя одновременно указать связанную привычку и вознаграждение.")

        # Периодичность не должна быть реже 1 раза в 7 дней
        if data.get('periodicity', 8) > 7:
            raise serializers.ValidationError("Периодичность должна быть не реже одного раза в 7 дней.")

        # Связанной привычкой может быть только приятная привычка
        if data.get('linked_habit') and not data['linked_habit'].is_pleasant:
            raise serializers.ValidationError("Связанной привычкой может быть только приятная привычка.")

        # Приятной привычке нельзя назначить связанную привычку или вознаграждение
        if data.get('is_pleasant') and (data.get('linked_habit') or data.get('reward')):
            raise serializers.ValidationError("Приятной привычке нельзя назначить связанную привычку или вознаграждение.")

        return data