import os
from django.conf import settings
from .models import Product

def generate_and_save_audio(product_id):
    product = Product.objects.get(pk=product_id)

    # 🔊 Допустим, здесь ты сам генерируешь .mp3 или скачиваешь его с сайта синтезатора
    text = product.name
    audio_path = os.path.join(settings.MEDIA_ROOT, f"{product_id}_audio.mp3")

    # Пример: записать заглушку (в реальности — скачиваешь из браузера или API)
    with open(audio_path, 'wb') as f:
        f.write(b'MP3 DATA HERE')

    # Сохраняем путь в поле модели
    product.audio_file.name = f"{product_id}_audio.mp3"
    product.save()
