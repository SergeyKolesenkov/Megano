from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Review
from ..catalog.models import Product
from django.utils import timezone

from .serializers import ReviewSerializer

class ReviewView(APIView):
    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        reviews = Review.objects.filter(product=product)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    def post(self, request, product_id):
        if not request.user.is_authenticated:
            return Response(
                {'detail': 'Требуется авторизация'},
                status=status.HTTP_403_FORBIDDEN
            )

        product = get_object_or_404(Product, pk=product_id)

        data = request.data.copy()
        data['product'] = product.id
        data['author'] = request.user.id
        data['date'] = timezone.localtime().strftime('%Y-%m-%d %H:%M:%S')

        serializer = ReviewSerializer(data=data)

        if serializer.is_valid():
            review = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
