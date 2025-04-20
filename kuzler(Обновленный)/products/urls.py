from django.urls import path
from .views import (
    ProductListCreateView,
    ProductDetailView,
    NFCAssignView,  # Это класс APIView
    get_product_by_nfc,
    get_product_by_nfc_from_query,
    download_audio,
    play_audio,
    arduino_data,
    # generate_audio_for_product и UploadAudio удалены, так как их функционал
    # теперь встроен в ProductListCreateView
)

urlpatterns = [
    # Товары
    path('products/', ProductListCreateView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    # NFC
    path('assign-nfc/', NFCAssignView.as_view(), name='nfc-assign'),  # Используем .as_view() для класса
    path('nfc/<str:uid>/', get_product_by_nfc, name='nfc-detail'),

    # Аудио
    path('audio/download/<int:product_id>/', download_audio, name='audio-download'),
    path('audio/play/<int:product_id>/', play_audio, name='audio-play'),

    # Специальные endpoints
    path('arduino/', arduino_data, name='arduino-api'),
    path('', get_product_by_nfc_from_query, name='nfc-query'),
]