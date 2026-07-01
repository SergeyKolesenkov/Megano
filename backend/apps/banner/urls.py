from django.urls import path
from .views import BannersView

urlpatterns = [
    path('banners/', BannersView.as_view(), name='banners'),
]