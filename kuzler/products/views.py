import os
from django.http import FileResponse, HttpResponseBadRequest, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics

from .models import Product, NFCTag
from .serializers import ProductSerializer
from .utils import generate_and_save_audio


# 🎧 Аудио по UID метке
@api_view(['GET'])
@permission_classes([AllowAny])
def play_audio(request):
    nfc_uid = request.GET.get('id')

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
@permission_classes([AllowAny])
def get_product_by_nfc(request, uid):
    try:
        tag = NFCTag.objects.get(uid=uid)
        product = tag.product
        data = {
            'nfc_uid': tag.uid,
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
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        product = serializer.save()
        print(f"[DEBUG] Создан продукт: {product.name}, ID: {product.id}")


# 🔍 Детали конкретного товара
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


# 📎 Привязка NFC к товару
@api_view(['POST'])
@permission_classes([AllowAny])
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


# 🗣 Генерация аудио из текста и сохранение
@api_view(['POST'])
@permission_classes([AllowAny])
def generate_audio_for_product(request):
    product_id = request.data.get('product_id')
    if not product_id:
        return Response({'error': 'product_id обязателен'}, status=400)

    try:
        generate_and_save_audio(product_id)
        return Response({'status': 'Аудио создано'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

class UploadAudio(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get("file")
        if file:
            with open(f"media/{file.name}", "wb+") as dest:
                for chunk in file.chunks():
                    dest.write(chunk)
            return Response({"status": "success"})
        return Response({"error": "no file"}, status=400)
from django.shortcuts import get_object_or_404

@api_view(['GET'])
@permission_classes([AllowAny])
def download_audio_by_product_id(request, id):
    product = get_object_or_404(Product, pk=id)

    if not product.audio_file:
        return Response({'error': 'У товара нет аудиофайла'}, status=404)

    audio_path = product.audio_file.path
    if not os.path.exists(audio_path):
        return Response({'error': 'Файл не найден на сервере'}, status=404)

    return FileResponse(open(audio_path, 'rb'), content_type='audio/mpeg')
