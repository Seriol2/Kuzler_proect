from django.contrib import admin
from .models import Product, NFCTag

# Регистрация моделей в административной панели
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')  # Показывать имя и цену в списке товаров
    search_fields = ['name']          # Возможность поиска по имени товара

@admin.register(NFCTag)
class NFCTagAdmin(admin.ModelAdmin):
    list_display = ('nfc_id', 'product', 'is_active')  # Показывать ID метки, связанный товар и статус активности
    list_filter = ('is_active',)                       # Добавляем фильтр по активности метки
    search_fields = ['nfc_id']                         # Возможность поиска по уникальному идентификатору метки
