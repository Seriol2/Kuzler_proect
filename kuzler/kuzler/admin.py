from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

def index(request):
    return HttpResponse("Добро пожаловать в Kuzler API 🚀")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('products.urls')),  # или другой путь
    path('', index),  # 👈 теперь / будет работать
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)