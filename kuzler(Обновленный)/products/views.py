from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product, NFCTag
from .serializers import ProductSerializer, NFCTagSerializer
from gtts import gTTS
import os
from django.conf import settings


class ProductListCreateView(generics.ListCreateAPIView):
    """
    Создание и просмотр списка товаров.
    Автоматически генерирует аудиоописание при создании товара.
    """
    queryset = Product.objects.all()
    print(queryset)
    serializer_class = ProductSerializer
    print(serializer_class)

    def perform_create(self, serializer):
        print(serializer)
        product = serializer.save()
        print(product)
        self._generate_audio(product)

    def _generate_audio(self, product):
        """Генерация аудиоописания товара"""
        text = f"{product.name}. Цена {product.price} рублей."
        tts = gTTS(text=text, lang='ru')

        # Создаем папку для аудио, если её нет
        audio_dir = os.path.join(settings.MEDIA_ROOT, 'product_audio')
        os.makedirs(audio_dir, exist_ok=True)

        # Сохраняем аудиофайл
        filename = f"product_{product.id}.mp3"
        filepath = os.path.join(audio_dir, filename)
        tts.save(filepath)

        # Сохраняем путь к файлу в модели
        product.audio_file = os.path.join('product_audio', filename)
        product.save()


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Просмотр, обновление и удаление конкретного товара"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class NFCAssignView(APIView):
    """Привязка NFC-метки к товару"""

    def post(self, request):
        uid = request.data.get('uid')
        product_id = request.data.get('product_id')

        if not uid or not product_id:
            return Response(
                {'error': 'Необходимо указать uid и product_id'},
                status=status.HTTP_400_BAD_REQUEST
            )

        product = get_object_or_404(Product, id=product_id)

        # Создаем или обновляем NFC-метку
        nfc_tag, created = NFCTag.objects.get_or_create(
            uid=uid,
            defaults={'product': product}
        )

        if not created:
            nfc_tag.product = product
            nfc_tag.save()

        return Response(
            {'message': f'NFC-метка {uid} привязана к товару {product.name}'},
            status=status.HTTP_200_OK
        )


def get_product_by_nfc(request, uid):
    """
    Получение информации о товаре по UID NFC-метки.
    Доступ через URL: /nfc/<uid>/
    """
    try:
        nfc_tag = NFCTag.objects.get(uid=uid)
        product = nfc_tag.product
        serializer = ProductSerializer(product)
        return JsonResponse(serializer.data)
    except NFCTag.DoesNotExist:
        return JsonResponse(
            {'error': 'NFC-метка не найдена'},
            status=status.HTTP_404_NOT_FOUND
        )


def get_product_by_nfc_from_query(request):
    """
    Получение информации о товаре по UID NFC-метки через query-параметр.
    Доступ через URL: /?id=<uid>
    """
    uid = request.GET.get('id')
    if not uid:
        return JsonResponse(
            {'error': 'Необходимо указать параметр id'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        nfc_tag = NFCTag.objects.get(uid=uid)
        product = nfc_tag.product

        # Формируем упрощенный ответ
        response_data = {
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
            'audio_url': product.audio_file.url if product.audio_file else None,
            'nfc_uid': uid
        }

        return JsonResponse(response_data)
    except NFCTag.DoesNotExist:
        return JsonResponse(
            {'error': 'Товар для указанной NFC-метки не найден'},
            status=status.HTTP_404_NOT_FOUND
        )


def download_audio(request, product_id):
    """Скачивание аудиофайла товара"""
    product = get_object_or_404(Product, id=product_id)

    if not product.audio_file:
        return JsonResponse(
            {'error': 'Аудиофайл не найден'},
            status=status.HTTP_404_NOT_FOUND
        )

    return FileResponse(
        product.audio_file.open(),
        as_attachment=True,
        filename=f'product_{product.id}.mp3'
    )


def play_audio(request, product_id):
    """Воспроизведение аудиофайла товара"""
    product = get_object_or_404(Product, id=product_id)

    if not product.audio_file:
        return JsonResponse(
            {'error': 'Аудиофайл не найден'},
            status=status.HTTP_404_NOT_FOUND
        )

    return FileResponse(
        product.audio_file.open(),
        content_type='audio/mpeg'
    )


def arduino_data(request):
    """
    Упрощенный API для Arduino.
    Возвращает только название товара и цену по NFC UID.
    """
    uid = request.GET.get('uid')
    if not uid:
        return JsonResponse(
            {'error': 'Необходимо указать параметр uid'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        nfc_tag = NFCTag.objects.get(uid=uid)
        product = nfc_tag.product
        return JsonResponse({
            'product_name': product.name,
            'price': str(product.price)
        })
    except NFCTag.DoesNotExist:
        return JsonResponse(
            {'error': 'NFC-метка не найдена'},
            status=status.HTTP_404_NOT_FOUND
        )