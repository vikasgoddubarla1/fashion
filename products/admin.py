from django.contrib import admin
from .models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'sale_price', 'original_price')
    list_display_links = ('id', 'title', 'sale_price', 'original_price')
# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)