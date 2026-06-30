from django.urls import path
from .views import ReviewView

urlpatterns = [
    path('product/<int:product_id>/reviews/', ReviewView.as_view(), name='review-list-create'),
]