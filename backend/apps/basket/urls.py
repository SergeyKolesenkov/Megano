from django.urls import path
from .views import BasketView, CartView

urlpatterns = [
    path('basket/<int:pk>/', BasketView.as_view(), name='basket-detail'),
    path('basket/', BasketView.as_view(), name='basket'),
    path('cart/', CartView.as_view(), name='cart'),
]