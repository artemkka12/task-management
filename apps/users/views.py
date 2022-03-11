from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.permissions import IsSuperUser
from apps.users.serializers import UserSerializer, GetTokenSerializer


def auth(request):
    return render(request, template_name='oauth.html')


def profile(request):
    return render(request, template_name='profile.html')


class UserRegisterView(GenericAPIView):
    serializer_class = UserSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(username=serializer.validated_data['email'])
        user.set_password(serializer.validated_data['password'])
        user.save()

        return Response(UserSerializer(user).data)


class UserListView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsSuperUser)


class TokenObtainView(TokenObtainPairView):
    serializer_class = GetTokenSerializer
