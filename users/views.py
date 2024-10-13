from rest_framework import viewsets, permissions
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    # Разрешить неавторизованным пользователям доступ к регистрации
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        return self.queryset.filter(is_active=Tru