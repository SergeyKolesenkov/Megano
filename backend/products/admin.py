from django.contrib import admin
from .models import Category, Product #Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']
    list_filter = ['parent', 'is_active']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'purchases_count', 'limited_edition']
    list_filter = ['category', 'limited_edition', 'is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['purchases_count']

# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ['product', 'user', 'rating', 'created_at']
#     list_filter = ['rating', 'created_at']
#     readonly_fields = ['created_at']