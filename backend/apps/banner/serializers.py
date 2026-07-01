from rest_framework import serializers
from .models import Banner

class BannerSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = [
            'id', 'title', 'description', 'images', 'url',
            'product_id', 'category', 'price'
        ]

    def get_images(self, obj):
        if obj.image:
            return [
                {
                    'src': obj.image.url,
                    'alt': obj.title or 'Banner image'
                }
            ]
        return []
