from rest_framework import serializers
from apps.catalog.serializers import ProductSerializer
from apps.orders.models import OrderItem, Order


class OrderSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    createdAt = serializers.DateTimeField(source='date', format='%Y-%m-%d %H:%M:%S', read_only=True)
    deliveryType = serializers.CharField(source='delivery_type', required=False, allow_blank=True)
    paymentType = serializers.CharField(source='payment_type', required=False, allow_blank=True)
    totalCost = serializers.DecimalField(source='total_cost', max_digits=10, decimal_places=2, read_only=True)
    fullName = serializers.CharField(source='customer.fullName', read_only=True, default="")
    email = serializers.EmailField(source='customer.email', read_only=True, default="")
    phone = serializers.CharField(source='customer.phone', read_only=True, default="")
    class Meta:
        model = Order
        fields = [
            'id', 'createdAt',
            'fullName', 'email', 'phone',
            'deliveryType', 'paymentType', 'totalCost',
            'status', 'city', 'address', 'products'
        ]


    def get_products(self, obj):

        result = []
        for item in obj.items.all():
            product = item.product
            if product:
                result.append({
                    'id': product.id,
                    'category': product.category_id,
                    'price': str(product.price),
                    'title': product.title,
                    'freeDelivery': product.freeDelivery,
                    'images': [
                        {'src': img.src.url if hasattr(img.src, 'url') else img.src, 'alt': img.alt}
                        for img in product.images.all()
                    ],
                    'tags': [{'id': t.id, 'name': t.name} for t in product.tags.all()],
                    'rating': product.rating,
                    'count': item.count,  # Подмешиваем количество из промежуточной таблицы
                })
        return result

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # <-- Используем его
    item_total = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'count', 'item_total']

    def get_item_total(self, obj):
        return float(obj.product.price * obj.count)