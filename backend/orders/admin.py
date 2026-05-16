from django.contrib import admin
from .models import Order, OrderItem #, DeliveryMethod, PaymentMethod

# @admin.register(DeliveryMethod)
# class DeliveryMethodAdmin(admin.ModelAdmin):
#     list_display = ['name', 'price', 'is_active']
#     list_filter = ['is_active']
#     search_fields = ['name']
#     readonly_fields = ['created_at', 'updated_at']
#
# @admin.register(PaymentMethod)
# class PaymentMethodAdmin(admin.ModelAdmin):
#     list_display = ['name', 'is_active']
#     list_filter = ['is_active']
#     search_fields = ['name']
#     readonly_fields = ['created_at', 'updated_at']

# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     extra = 0
#     readonly_fields = ['product', 'price', 'quantity', 'total_price']
#     can_delete = False
#
# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = [
#         'id', 'user', 'total_amount', 'status',
#         'delivery_method', 'payment_method', 'created_at'
#     ]
#     list_filter = [
#         'status', 'delivery_method', 'payment_method',
#         'created_at', 'is_paid'
#     ]
#     search_fields = ['id', 'user__username', 'user__email']
#     readonly_fields = [
#         'created_at', 'updated_at', 'total_amount',
#         'payment_status', 'payment_error'
#     ]
#     fieldsets = (
#         ('Основные данные', {
#             'fields': ('user', 'status', 'is_paid')
#         }),
#         ('Доставка', {
#             'fields': ('delivery_method', 'address')
#         }),
#         ('Оплата', {
#             'fields': ('payment_method', 'payment_status', 'payment_error')
#         }),
#         ('Финансовая информация', {
#             'fields': ('total_amount',)
#         }),
#         ('Даты', {
#             'fields': ('created_at', 'updated_at')
#         }),
#     )
#     inlines = [OrderItemInline]
