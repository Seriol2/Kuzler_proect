from django.urls import path
from .views import (
    ProductListCreateView,
    ProductDetailView,
    NFCAssignView,
    get_product_by_nfc,
    play_audio,
    UploadAudio,
    generate_audio_for_product,
    download_audio_by_product_id,
)

urlpatterns = [
    # 📦 Продукты
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    # 📎 NFC
    path('nfc/assign/', NFCAssignView, name='nfc-assign'),
    path('nfc/<str:uid>/', get_product_by_nfc, name='nfc-detail'),

    # 🔊 Аудио
    path('audio/', play_audio, name='play-audio'),
    path('audio/product/<int:id>/', download_audio_by_product_id, name='download-audio-by-id'),
    path('upload/', UploadAudio.as_view(), name='upload-audio'),
    path('generate_audio/', generate_audio_for_product, name='generate-audio'),
]
