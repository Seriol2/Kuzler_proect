from django.contrib import admin
from .models import Product

# Регистрируем модель Product в админке
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'price')  # Поля, которые отображаются в списке товаров
    search_fields = ('code', 'name')  # Поиск по коду и названию товара
    list_filter = ('price',)  # Фильтрация по цене товара
