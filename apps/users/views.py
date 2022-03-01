from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.users.permissions import IsSuperUser
from apps.users.serializers import UserSerializer


class UserRegisterView(GenericAPIView):
    serializer_class = UserSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        users = User.objects.all()
        for user in users:
            if serializer.validated_data['email'] == user.username:
                raise ValidationError("This email is already in use")
        user = serializer.save(username=serializer.validated_data['email'])

        user.set_password(serializer.validated_data['password'])
        user.save()

        return Response(UserSerializer(user).data)


class UserListView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsSuperUser)
