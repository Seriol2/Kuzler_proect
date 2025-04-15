from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    audio_file = serializers.FileField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'audio_file']
