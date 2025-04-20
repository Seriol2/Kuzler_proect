from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    audio_file = models.FileField(upload_to='product_audio/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Product(models.Model):
        name = models.CharField(
            max_length=255,
            verbose_name="Название",
            help_text="Обязательное поле, максимум 255 символов"
        )

        # ... остальные поля ...

        def save(self, *args, **kwargs):
            # Нормализация текста перед сохранением
            if self.name:
                self.name = unicodedata.normalize('NFKC', str(self.name))
            super().save(*args, **kwargs)
class NFCTag(models.Model):
    uid = models.CharField(max_length=255, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='nfc_tags')

    def __str__(self):
        return f'NFC Tag {self.uid} → {self.product.name}'
