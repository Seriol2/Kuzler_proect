from gtts import gTTS

text = "Привет, как дела?"
tts = gTTS(text=text, lang='ru')
tts.save("output.mp3")

print("✅ Аудио сохранено в output.mp3")
