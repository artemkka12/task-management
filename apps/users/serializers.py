from rest_framework import serializers
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import User, TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')


class GetTokenSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD
    email = serializers.EmailField()
    password = serializers.CharField()

    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)
        return {
            "refresh": str(token),
            "access": str(token.access_token)
        }

    def validate(self, attrs):
        data = {
            self.username_field: attrs[self.username_field]
        }

        user = User.objects.get(**data)

        if not user.is_active:
            raise serializers.ValidationError("User isn`t active")
        if user.check_password(attrs["password"]):
            return self.get_token(user)
        return AuthenticationFailed("Invalid data")
