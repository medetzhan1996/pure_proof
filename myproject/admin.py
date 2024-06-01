from django.contrib import admin
from .models import Product, ScanHistory, Review, Post, ChatMessage

class ProductAdmin(admin.ModelAdmin):
    list_display = ('barcode', 'name', 'description', 'verified')
    search_fields = ('barcode', 'name')
    list_filter = ('verified',)

class ScanHistoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'scan_date')
    search_fields = ('product__name', 'user__username')
    list_filter = ('scan_date',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'review_text', 'rating', 'review_date')
    search_fields = ('product__name', 'user__username', 'review_text')
    list_filter = ('rating', 'review_date')

# Регистрация моделей с соответствующими классами администрирования
admin.site.register(Product, ProductAdmin)
admin.site.register(ScanHistory, ScanHistoryAdmin)
admin.site.register(Review, ReviewAdmin)

admin.site.register(Post)
admin.site.register(ChatMessage)
