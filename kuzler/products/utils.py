# utils.py
from gtts import gTTS
from django.core.files import File
from .models import Product
import os
import tempfile


def generate_and_save_audio(product_id):
    product = Product.objects.get(id=product_id)
    text = f"{product.name}, цена {product.price} рублей"

    print(f"[AUDIO DEBUG] Генерация для: {text}")

    # Генерируем аудио
    tts = gTTS(text=text, lang='ru')

    # Создаём временный файл
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
        tmp_path = tmp_file.name
        tts.save(tmp_path)
        print(f"[AUDIO DEBUG] Аудиофайл создан по пути: {tmp_path}")

    # Проверяем размер
    print(f"[AUDIO DEBUG] Размер файла: {os.path.getsize(tmp_path)} байт")

    # Сохраняем в модель
    with open(tmp_path, 'rb') as f:
        product.audio_file.save(f"audio_{product_id}.mp3", File(f), save=True)

    print(f"[AUDIO DEBUG] Аудиофайл сохранён: {product.audio_file.path}")

    # Удаляем временный файл
    os.remove(tmp_path)
