from django.urls import path
from .views import (
    ProductListCreateView,
    ProductDetailView,
    UploadAudio,
    play_audio,
    download_audio_by_product_id,
    generate_audio_for_product,
    NFCAssignView,
    get_product_by_nfc,
    get_product_by_nfc_from_query,
    arduino_data,
)

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('upload-audio/', UploadAudio.as_view(), name='upload-audio'),
    path('play-audio/', play_audio, name='play-audio'),
    path('download-audio/<int:id>/', download_audio_by_product_id, name='download-audio'),
    path('generate-audio/', generate_audio_for_product, name='generate-audio'),
    path('assign-nfc/', NFCAssignView, name='assign-nfc'),
    path('nfc/<str:uid>/', get_product_by_nfc, name='get-product-by-nfc'),
    path('arduino/', arduino_data, name='arduino-data'),

    # 👇 ВАЖНО: только одна строка для root ('')
    path('', get_product_by_nfc_from_query, name='get-product-by-nfc-query'),
]
