from rest_framework import serializers
from django.db.models import Sum
from .models import Basket, BasketItem, Product
from ..catalog.serializers import ProductSerializer


class BasketItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    class Meta:
        model = BasketItem
        fields = ['id', 'product', 'count', 'product_id']


class BasketSerializer(serializers.ModelSerializer):
    total_quantity = serializers.SerializerMethodField()
    basket_items = BasketItemSerializer(many=True, read_only=True)
    basketCount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Basket
        # Убираем total_price, если его нет в модели, чтобы не было ошибок
        fields = ['id', 'total_quantity', 'basket_items', 'basketCount']

    def get_total_quantity(self, obj):
        total = obj.basket_items.aggregate(Sum('count'))['count__sum']
        return total or 0

    def get_basketCount(self, obj):
        total_price = sum(item.product.price * item.count for item in obj.basket_items.all())
        return {"price": float(total_price)}