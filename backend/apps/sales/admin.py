from django import forms
from django.contrib import admin
from django.utils.html import format_html
from apps.sales.models import Sale, SaleProduct

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['product', 'sale_price', 'date_from', 'date_to']
    search_fields = ['product__title']
    list_filter = ['date_from', 'date_to']
