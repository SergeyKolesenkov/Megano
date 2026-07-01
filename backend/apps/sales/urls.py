from django.urls import path
from .views import SalesView, sales_page

urlpatterns = [
    path('sales/', SalesView.as_view(), name='sales'),
]