from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer


class CategoriesView(APIView):
    def get(self, request):
        queryset = Category.objects.prefetch_related(
            'images',
            'subcategories',
            'subcategories__images',
            'products',
            'products__images',
            'products__tags',
        )
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def get(self, request):
        queryset = Category.objects.prefetch_related('subcategories', 'images', 'subcategories__images')
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)