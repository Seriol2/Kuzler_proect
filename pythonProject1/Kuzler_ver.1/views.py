from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, NFCTagViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'nfc-tags', NFCTagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
