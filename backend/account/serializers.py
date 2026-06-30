from .models import Avatar
from rest_framework import serializers
from .models import Profile


# class AvatarUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['avatar']
#
# class AvatarSerializer(serializers.ModelSerializer):
#     src = serializers.ImageField(read_only=True)
#
#     class Meta:
#         model = Avatar
#         fields = ["src", "alt"]
#         extra_kwargs = {
#             'alt': {'required': False}
#         }



class ProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('phone', 'email', 'fullName', 'avatar')

    def get_avatar(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return None
