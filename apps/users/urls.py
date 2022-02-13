from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users.views import UserRegisterView, UserListView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='token-register'),
    path('token/', TokenObtainPairView.as_view(), name='token-obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('users-list/', UserListView.as_view(), name='users-list'),
]
