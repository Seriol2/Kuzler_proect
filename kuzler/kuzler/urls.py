from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def index(request):
    return HttpResponse("Добро пожаловать в Kuzler API 🚀")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('products.urls')),  # или другой путь
    path('', index),  # 👈 теперь / будет работать
]
