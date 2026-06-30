from django.urls import path
from apps.catalog.views import ProductView, ProductDetailsView, PopularProductsView, LimitedProductsView

urlpatterns = [
    path('catalog/<int:subcategory_id>/', ProductView.as_view(), name='products_by_subcategory'),
    path('catalog/', ProductView.as_view(), name='catalog',),
    path('product/<int:product_id>/', ProductDetailsView.as_view(), name='product_details'),
    path('products/popular/', PopularProductsView.as_view(), name='popular-products'),
    path('products/limited/', LimitedProductsView.as_view(), name='limited-products'),
    ]