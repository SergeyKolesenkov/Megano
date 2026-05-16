from django.db import models
from django.conf import settings
from products.models import Product
from django.utils.translation import gettext_lazy as _

class Order(models.Model):
    DELIVERY_CHOICES = [
        ('pickup', _('Самовывоз')),
        ('courier', _('Курьерская доставка')),
        ('post', _('Почта России')),
    ]

    PAYMENT_CHOICES = [
        ('card', _('Банковская карта')),
        ('cash', _('Наличными')),
        ('online', _('Онлайн-оплата')),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', _('Ожидает оплаты')),
        ('paid', _('Оплачен')),
        ('failed', _('Ошибка оплаты')),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('пользователь')
    )
    products = models.ManyToManyField(Product, verbose_name=_('товары'), through='OrderItem')
    delivery_method = models.CharField(_('способ доставки'), max_length=20, choices=DELIVERY_CHOICES)
    payment_method = models.CharField(_('способ оплаты'), max_length=20, choices=PAYMENT_CHOICES)
    comment = models.TextField(_('комментарий'), blank=True)
    payment_status = models.CharField(
        _('статус оплаты'),
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )
    error = models.TextField(_('ошибка'), blank=True)

    created_at = models.DateTimeField(_('дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('дата обновления'), auto_now=True)

    class Meta:
        verbose_name = _('заказ')
        verbose_name_plural = _('заказы')

    def __str__(self):
        return f'Заказ #{self.id} от {self.user.get_full_name()}'



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_('количество'), default=1)
    price = models.DecimalField(_('цена'), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _('позиция заказа')
        verbose_name_plural = _('позиции заказа')



class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('пользователь'),
        null=True,
        blank=True
    )
    session_key = models.CharField(_('сессия'), max_length=40, unique=True, null=True, blank=True)
    products = models.ManyToManyField(Product, verbose_name=_('товары'), through='CartItem')

    class Meta:
        verbose_name = _('корзина')
        verbose_name_plural = _('корзины')

    def __str__(self):
        if self.user:
            return f'Корзина пользователя {self.user.get_full_name()}'
        return f'Корзина сессии {self.session_key}'



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_('количество'), default=1)

    class Meta:
        verbose_name = _('позиция корзины')
        verbose_name_plural = _('позиции корзины')