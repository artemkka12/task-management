from rest_framework.routers import DefaultRouter

from apps.gallery.views import PictureViewSet

router = DefaultRouter()

router.register(r'pictures', PictureViewSet, basename='pictures')

urlpatterns = router.urls
