from django.db import models


class Product(models.Model):
    code = models.CharField(max_length=6, unique=True)  # Код товара, уникальный, длина 6 символов
    name = models.CharField(max_length=255)  # Название товара
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена товара (до 99999999.99)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
