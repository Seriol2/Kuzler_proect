from rest_framework import serializers
from .models import Product, NFCTag


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class NFCTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFCTag
        fields = '__all__'
