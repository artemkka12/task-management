from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_util.decorators import serialize_decorator

from apps.users.serializers import UserSerializer


class UserRegisterView(GenericAPIView):
    serializer_class = UserSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    @serialize_decorator(UserSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data

        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_superuser=True,
            is_staff=True
        )

        user.set_password(validated_data['password'])
        user.save()

        return Response(UserSerializer(user).data)


class UserListView(GenericAPIView):
    serializer_class = UserSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        users = User.objects.all()

        return Response(UserSerializer(users, many=True).data)
