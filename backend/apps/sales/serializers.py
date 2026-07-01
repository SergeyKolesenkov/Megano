from rest_framework import serializers

from rest_framework import serializers
from .models import Sale

class SaleSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='product.title', read_only=True)
    price = serializers.DecimalField(source='original_price', max_digits=10, decimal_places=2, read_only=True)
    salePrice = serializers.DecimalField(source='sale_price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Sale
        fields = ['title', 'price', 'salePrice']
