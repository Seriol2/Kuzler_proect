"""
URL configuration for kuzler project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('products.urls')),  # Все API по namespace 'products'
]

# Отдача медиафайлов (например, mp3)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
