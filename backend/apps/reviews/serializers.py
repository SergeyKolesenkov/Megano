from rest_framework import serializers
from apps.reviews.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    author_avatar = serializers.SerializerMethodField()
    date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = Review
        fields = [
            'id', 'product', 'author', 'author_name', 'author_avatar', 'text', 'rate',
            'date', 'updated', 'email'
        ]
        read_only_fields = ['date', 'updated']

    def get_author_avatar(self, obj):
        profile = getattr(obj.author, 'profile', None)
        if profile and profile.avatar:
            return profile.avatar.url
        return None