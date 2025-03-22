from django.db import models

# Модель для продуктов
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.name

# Модель для NFC-меток
class NFCTag(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    nfc_id = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"NFC Tag for {self.product}"
