from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from . import settings
from apps.users.views import auth_github, profile_github, auth_google

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Enjoy",
    ),
    validators=['ssv'],
    public=True,
    permission_classes=(AllowAny,)
)

urlpatterns = [
                  path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  path('admin/', admin.site.urls),

                  path('', include('social_django.urls', namespace='social')),
                  path('accounts/', include('allauth.urls')),
                  path('auth/github/', auth_github),
                  path('accounts/profile/', profile_github),
                  path('auth/google/', auth_google),

                  path('user/', include('apps.users.urls')),
                  path('', include('apps.tasks.urls')),
                  path('comment/', include('apps.comments.urls')),
                  path('gallery/', include('apps.gallery.urls')),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
