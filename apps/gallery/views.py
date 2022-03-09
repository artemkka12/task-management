from minio import Minio
from rest_framework import parsers, renderers
from rest_framework.viewsets import ModelViewSet

from apps.gallery.models import Picture
from apps.gallery.serializers import PictureSerializer


class PictureViewSet(ModelViewSet):
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

    # def post(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     validated_data = serializer.validated_data
    #
    #     client = Minio(
    #         "10.1.1.174:9000",
    #         access_key="H0T3P3FNGDTFFSR7353I",
    #         secret_key="lF7Vc8jiRntTaIVlYAX+3+5PUey+5xmrcvpegtzd",
    #         secure=False
    #     )
    #
    #
    #
