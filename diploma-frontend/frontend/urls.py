from django.urls import path
from django.views.generic import TemplateView

from account.views import sign_in, sign_up

# from backend.accounts.views import sign_in, sign_up


urlpatterns = [
    path('', TemplateView.as_view(template_name="frontend/index.html")),
    path('about/', TemplateView.as_view(template_name="frontend/about.html")),
    path('cart/', TemplateView.as_view(template_name="frontend/cart.html")),
    path('catalog/', TemplateView.as_view(template_name="frontend/catalog.html")),
    path('catalog/<int:id>/', TemplateView.as_view(template_name="frontend/catalog.html")),
    path('history-order/', TemplateView.as_view(template_name="frontend/historyorder.html")),
    path('order-detail/<int:id>/', TemplateView.as_view(template_name="frontend/oneorder.html")),
    path('order/<int:id>/', TemplateView.as_view(template_name="frontend/order.html")),
    path('payment/<int:id>/', TemplateView.as_view(template_name="frontend/payment.html")),
    path('payment-someone/', TemplateView.as_view(template_name="frontend/paymentsomeone.html")),
    path('product/<int:id>/', TemplateView.as_view(template_name="frontend/product.html")),
    path('profile/', TemplateView.as_view(template_name="frontend/profile.html")),
    path('progress-payment/', TemplateView.as_view(template_name="frontend/progressPayment.html")),
    path('sales/', TemplateView.as_view(template_name="frontend/sales.html")),
    path('sale/', TemplateView.as_view(template_name='frontend/profile.html'))
    # path('sign-in/', TemplateView.as_view(template_name="frontend/signIn.html"), name='login_page'),
    # path('sign-up/', TemplateView.as_view(template_name="frontend/signUp.html"), name='register_page'),

    # path('sign-in/', sign_in, name='sign_in'),
    # path('sign-up/', sign_up, name='sign_up'),
]
