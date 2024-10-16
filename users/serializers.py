from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "telegram_chat_id",
            "password",
        ]

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            telegram_chat_id=validated_data.get('telegram_chat_id', None)
        )
        user.set_password(validated_data['password'])  # Хеширование пароля
        user.save()
        return user
