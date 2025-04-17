from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product, NFCTag
from .serializers import ProductSerializer, NFCTagSerializer
from gtts import gTTS
import os


# Список и создание товаров
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Получение, обновление, удаление товара
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Загрузка аудио к товару
class UploadAudio(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        audio_file = request.FILES.get('audio_file')

        if not product_id or not audio_file:
            return Response({'error': 'Missing product_id or audio_file'}, status=400)

        product = get_object_or_404(Product, id=product_id)
        product.audio_file = audio_file
        product.save()

        return Response({'message': 'Audio uploaded successfully'})


# Проигрывание аудио
def play_audio(request):
    product_id = request.GET.get('product_id')
    product = get_object_or_404(Product, id=product_id)

    if product.audio_file:
        return FileResponse(product.audio_file.open(), content_type='audio/mpeg')
    else:
        return JsonResponse({'error': 'No audio found for this product'}, status=404)


# Скачивание аудио
def download_audio_by_product_id(request, id):
    product = get_object_or_404(Product, id=id)
    if product.audio_file:
        return FileResponse(product.audio_file.open(), as_attachment=True)
    else:
        return JsonResponse({'error': 'Audio file not found'}, status=404)


# Генерация аудио из текста
def generate_audio_for_product(request):
    product_id = request.GET.get('product_id')
    product = get_object_or_404(Product, id=product_id)

    text = f"{product.name}, цена: {product.price} рублей"
    tts = gTTS(text=text, lang='ru')
    filename = f"{product.id}_generated.mp3"
    filepath = os.path.join('media/product_audio', filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    tts.save(filepath)

    product.audio_file = f'product_audio/{filename}'
    product.save()

    return JsonResponse({'message': 'Audio generated', 'file': product.audio_file.url})


# Привязка NFC к товару
def NFCAssignView(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        product_id = request.POST.get('product_id')

        if not uid or not product_id:
            return JsonResponse({'error': 'Missing uid or product_id'}, status=400)

        product = get_object_or_404(Product, id=product_id)
        nfc_tag, created = NFCTag.objects.get_or_create(uid=uid, defaults={'product': product})
        if not created:
            nfc_tag.product = product
            nfc_tag.save()

        return JsonResponse({'message': 'NFC tag assigned'})


# Получение товара по UID через путь
def get_product_by_nfc(request, uid):
    try:
        nfc_tag = NFCTag.objects.get(uid=uid)
        product = nfc_tag.product
        data = ProductSerializer(product).data
        return JsonResponse(data)
    except NFCTag.DoesNotExist:
        return JsonResponse({'error': 'NFC tag not found'}, status=404)


# Получение товара по UID через query-параметр ?id=
def get_product_by_nfc_from_query(request):
    uid = request.GET.get('id')
    if not uid:
        return JsonResponse({'error': 'Missing id in query'}, status=400)
    try:
        tag = NFCTag.objects.get(uid=uid)
        product = tag.product
        return JsonResponse({
            'product': product.name,
            'price': str(product.price),
            'id': product.id
        })
    except NFCTag.DoesNotExist:
        return JsonResponse({'error': 'NFC tag not found'}, status=404)


# Для Arduino
def arduino_data(request):
    uid = request.GET.get('uid')
    try:
        tag = NFCTag.objects.get(uid=uid)
        product = tag.product
        return JsonResponse({
            'product_name': product.name,
            'price': str(product.price),
        })
    except NFCTag.DoesNotExist:
        return JsonResponse({'error': 'Tag not found'}, status=404)
