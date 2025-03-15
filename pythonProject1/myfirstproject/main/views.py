from django.shortcuts import render
from django.http import JsonResponse, FileResponse, Http404
from django.conf import settings
import os

def index(request):
    data = {
        "message": "Hi. It's JSON",
        "status": "200"
    }
    return JsonResponse(data)

def image_view(request):
    image_path = os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'imag_to_test.py')
    try:
        return FileResponse(open(image_path, 'rb'), content_type='image/png')
    except FileNotFoundError:
        raise Http404("Изображение не найдено")