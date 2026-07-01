from django.urls import path
from .views import TagsView

urlpatterns = [
    path('tags/', TagsView.as_view(), name='tags'),
]