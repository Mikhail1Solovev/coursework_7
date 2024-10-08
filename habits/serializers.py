
from rest_framework import serializers
from .models import Habit

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user',)

    def validate(self, data):
        if data.get('related_habit') and data.get('reward'):
            raise serializers.ValidationError("You can either specify a related habit or a reward, not both.")
        if data.get('duration', 0) > 120:
            raise serializers.ValidationError("The duration cannot exceed 120 seconds.")
        return data
