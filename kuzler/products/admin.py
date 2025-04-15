from django.contrib import admin
from django.utils.html import format_html
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'audio_player', 'created_at')
    readonly_fields = ('audio_player',)
    list_filter = ('created_at',)
    search_fields = ('name',)

    def audio_player(self, obj):
        if obj.audio_file:
            return format_html(
                '<audio controls style="max-width: 200px;"><source src="{}" type="audio/mpeg">Твой браузер не поддерживает аудио.</audio>',
                obj.audio_file.url
            )
        return "Нет аудио"
    audio_player.short_description = "🔊 Аудио"

admin.site.register(Product, ProductAdmin)
