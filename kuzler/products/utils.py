# utils.py
from gtts import gTTS
from django.core.files import File
from .models import Product
import os
import tempfile


def generate_and_save_audio(product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        print(f"[AUDIO ERROR] Продукт с ID {product_id} не найден.")
        return

    text = f"{product.name}, цена {product.price} рублей"

    print(f"[AUDIO DEBUG] Генерация для: {text}")

    try:
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
            django_file = File(f)
            product.audio_file.save(f"audio_{product.id}.mp3", django_file, save=True)
            print(f"[AUDIO DEBUG] Аудиофайл сохранён в: {product.audio_file.path}")

    except Exception as e:
        print(f"[AUDIO ERROR] Ошибка при генерации/сохранении аудио: {e}")

    finally:
        # Удаляем временный файл
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
            print("[AUDIO DEBUG] Временный файл удалён.")
