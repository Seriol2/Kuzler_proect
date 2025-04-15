from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    audio_file = models.FileField(upload_to='audio/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # <-- вот это добавь

    def __str__(self):
        return self.name
    # Прямая связь с NFC
    nfc = models.ForeignKey(
        'NFCTag',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='linked_product'  # <-- уникальное имя для связи обратно
    )

    def __str__(self):
        return f"{self.name}"


class NFCTag(models.Model):
    uid = models.CharField(max_length=100, unique=True)

    # Обратная связь с Product (если нужно)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='nfc_tags'
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tag {self.uid} → {self.product.name}"
