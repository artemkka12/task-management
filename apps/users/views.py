from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from apps.users.serializers import UserSerializer


class UserRegisterView(GenericAPIView):
    serializer_class = UserSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(username=serializer.validated_data['email'])
        # validated_data = serializer.validated_data
        # other_users = User.objects.filter(email=validated_data['email'])
        # for user in other_users:
        #     if validated_data['email'] == user.email:
        #         raise ValidationError("This email is already in use")

        # user = User.objects.create(
        #     first_name=validated_data['first_name'],
        #     last_name=validated_data['last_name'],
        #     username=validated_data['email'],
        #     email=validated_data['email'],
        #     password=validated_data['password'],
        #     is_superuser=False,
        #     is_staff=True
        # )

        user.set_password(serializer.validated_data['password'])
        user.save()

        return Response(UserSerializer(user).data)


class UserListView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)
