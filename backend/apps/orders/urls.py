from django.urls import path

from .views import OrderView, OrderDetailView, OrderHistoryPageView

app_name = 'orders'

urlpatterns = [
    path('orders/', OrderView.as_view(), name='order-create'),
    path('orders/<int:id>/', OrderDetailView.as_view(), name='order-detail'),
    path('history-order/', OrderHistoryPageView.as_view(), name='history-order-page'),
]
