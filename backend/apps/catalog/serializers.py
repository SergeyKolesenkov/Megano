from rest_framework import serializers
from .models import Product, ProductImage, Tag
from ..reviews.models import Review
from ..tags.serializers import TagSerializer


class ProductImageSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['src', 'alt']

    def get_src(self, obj):
        return obj.src.url


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    rating = serializers.FloatField()

    class Meta:
        model = Product
        fields = [
            'id', 'category','subcategory', 'price', 'date', 'title', 'freeDelivery',
            'description', 'images','stock', 'tags', 'rating', 'sort_index'
            ]


