# products/views.py

import os
from django.http import FileResponse, HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics

from .models import Product, NFCTag
from .serializers import ProductSerializer

# 🎧 Аудио по UID метки
@api_view(['GET'])
def play_audio(request):
    nfc_uid = request.GET.get('id')  # id — это UID NFC метки

    if not nfc_uid:
        return HttpResponseBadRequest("Missing 'id' parameter")

    try:
        tag = NFCTag.objects.get(uid=nfc_uid)
        product = tag.product

        if not product.audio_file:
            return HttpResponse("Audio file not found", status=404)

        audio_path = product.audio_file.path

        if not os.path.exists(audio_path):
            return HttpResponse("Audio file missing", status=404)

        return FileResponse(open(audio_path, 'rb'), content_type='audio/mpeg')

    except NFCTag.DoesNotExist:
        return HttpResponse("NFCTag not found", status=404)


# 📦 Получить товар по UID NFC
@api_view(['GET'])
def get_product_by_nfc(request, uid):
    try:
        tag = NFCTag.objects.get(uid=uid)
        product = tag.product
        data = {
            'nfc_id': product.nfc_id,
            'name': product.name,
            'price': str(product.price),
        }
        return Response(data)
    except NFCTag.DoesNotExist:
        return Response({'error': 'Товар не найден'}, status=404)


# 📋 Список товаров / создание
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# 🔍 Детали конкретного товара
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# 📎 Привязка NFC к товару (если нужно)
@api_view(['POST'])
def NFCAssignView(request):
    uid = request.data.get('uid')
    product_id = request.data.get('product_id')

    if not uid or not product_id:
        return Response({'error': 'UID и product_id обязательны'}, status=400)

    try:
        product = Product.objects.get(pk=product_id)
        tag, created = NFCTag.objects.update_or_create(
            uid=uid,
            defaults={'product': product}
        )
        return Response({'status': 'assigned', 'product': product.name})
    except Product.DoesNotExist:
        return Response({'error': 'Продукт не найден'}, status=404)
