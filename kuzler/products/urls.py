from django.urls import path
from .views import (
    ProductListCreateView,
    ProductDetailView,
    NFCAssignView,
    get_product_by_nfc,
    play_audio
)

urlpatterns = [
    # Товары
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    # NFC
    path('nfc/assign/', NFCAssignView, name='nfc-assign'),  # Это функция
    path('nfc/<str:uid>/', get_product_by_nfc, name='nfc-detail'),

    # Аудио
    path('audio/', play_audio, name='play-audio'),
]
