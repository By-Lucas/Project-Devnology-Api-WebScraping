from django.contrib import admin
from products.models import Products, Category

class ProductsAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price', 'description']
    list_filter = []
    search_fields = ['price']
    filter_horizontal = []

admin.site.register(Products, ProductsAdmin)
admin.site.register(Category)