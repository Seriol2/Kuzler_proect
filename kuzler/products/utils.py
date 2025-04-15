import os
from gtts import gTTS
from django.core.files import File
from .models import Product  # ← вот это обязательно

def generate_and_save_audio(product_id):
    product = Product.objects.get(id=product_id)
    text = f"{product.name}, цена {product.price} рублей"

    print(f"[AUDIO DEBUG] Генерация для: {text}")

    audio_dir = "media/audio"
    os.makedirs(audio_dir, exist_ok=True)
    audio_path = os.path.join(audio_dir, f"audio_{product_id}.mp3")

    try:
        tts = gTTS(text=text, lang='ru')
        tts.save(audio_path)
        print(f"[AUDIO DEBUG] Аудиофайл создан по пути: {audio_path}")
        print(f"[AUDIO DEBUG] Размер файла: {os.path.getsize(audio_path)} байт")
    except Exception as e:
        print(f"[ERROR] Ошибка сохранения аудио: {e}")
        return

    with open(audio_path, 'rb') as f:
        product.audio_file.save(f"audio/audio_{product_id}.mp3", File(f), save=True)

    print(f"[AUDIO DEBUG] Аудиофайл сохранён: {product.audio_file.path}")
