from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from TooPath3.models import Track


class TracksList(APIView):
    def get_object(self, pk):
        obj = get_object_or_404(Track, pk=pk)
        self.check_object_permissions(self.request, obj=obj)
        return obj

    def post(self, request, pk):
        device = self.get_object(pk)
        return Response()
