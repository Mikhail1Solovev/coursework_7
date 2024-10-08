from rest_framework import serializers
from .models import Habit

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, data):
        if data.get('reward') and data.get('linked_habit'):
            raise serializers.ValidationError('Можно заполнить либо вознаграждение, либо связанную привычку, но не оба поля одновременно.')
        if data.get('execution_time') > 120:
            raise serializers.ValidationError('Время выполнения привычки не может превышать 120 секунд.')
        if data.get('periodicity') > 7:
            raise serializers.ValidationError('Периодичность выполнения привычки должна быть не реже одного раза в неделю.')
        return data
