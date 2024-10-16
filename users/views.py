from rest_framework import viewsets, permissions
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    # Разрешить неавторизованным пользователям доступ к регистрации
    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        return self.queryset.filter(is_active=True)

# Добавляем отдельный эндпоинт для регистрации пользователя
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
