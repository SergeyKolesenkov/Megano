from rest_framework import serializers
from .models import Specification

class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ['name', 'value']