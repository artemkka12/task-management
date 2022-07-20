from rest_framework import parsers, renderers
from rest_framework.viewsets import ModelViewSet

from apps.gallery.models import Picture
from apps.gallery.serializers import PictureSerializer


class PictureViewSet(ModelViewSet):
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer)
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
