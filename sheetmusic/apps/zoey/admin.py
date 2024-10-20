from django.contrib import admin
from .models import Product, ZProduct

admin.site.register(Product)

@admin.register(ZProduct)
class ZProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'id', 'created', 'modified')
