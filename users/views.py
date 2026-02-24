from rest_framework.generics import CreateAPIView

from users.models import User
from users.serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
