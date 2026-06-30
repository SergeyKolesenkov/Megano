from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Banner
from .serializers import BannerSerializer

class BannersView(APIView):
    def get(self, request):
        banners = Banner.objects.filter(is_active=True)
        serializer = BannerSerializer(banners, many=True)
        return Response(serializer.data)
