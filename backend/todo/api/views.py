from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, generics
from todo.api.serializer import TodoSerializer, UserSerializer
from todo.models import Todo
from pprint import pprint
# from user.models import ModelToken


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user.id)
        return qs
    # def get_queryset(self):
    #     res = self.request
    #     print(f'res = {res}')
    #     print(f'user = {res.user}')
    #     print(f'Авторизация: {self.request.headers.get("Authorization")}')


# классический вид
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

