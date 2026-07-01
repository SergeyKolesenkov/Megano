from rest_framework import serializers
from .models import Category, Subcategory
from apps.catalog.serializers import ProductSerializer
from ..catalog.models import Product


class SubcategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Subcategory
        fields = ['id', 'title', 'image']

    def get_image(self, obj):
        first_image = obj.images.first()
        if first_image:
            return {
                'src': first_image.src.url,
                'alt': first_image.alt or obj.title
            }
        return None

    def get_products(self, obj):
        products = Product.objects.filter(subcategory=obj)[0]  # ограничиваем выборку
        return ProductSerializer(products, many=True).data


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    subcategories = SubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'subcategories']

    def get_image(self, obj):
        first_image = obj.images.first()
        if first_image:
            return {
                'src': first_image.src.url,
                'alt': first_image.alt or obj.title
            }
        return None

    def get_products(self, obj):
        products = Product.objects.filter(category=obj)[0]  # ограничиваем выборку
        return ProductSerializer(products, many=True).data

