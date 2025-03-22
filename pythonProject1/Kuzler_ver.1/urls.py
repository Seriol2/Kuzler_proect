from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from myapp.views import ProductViewSet, NFCTagViewSet

# Создаем маршрутизатор для API
router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('nfc-tags', NFCTagViewSet, basename='nfctag')

urlpatterns = [
    # Маршрут для админки Django
    path('admin/', admin.site.urls),
    
    # Маршруты для API
    path('api/', include(router.urls)),
]
