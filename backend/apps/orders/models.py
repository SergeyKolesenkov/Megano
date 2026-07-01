from django.db import models

from account.models import Profile


class Order(models.Model):
    class Meta:
        ordering = ['-date']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    DELIVERY_CHOICES = [
        ('standard', 'Обычная'),
        ('express', 'Экспресс'),
    ]

    city = models.CharField('Город', max_length=100, blank=True)
    address = models.CharField('Адрес', max_length=100, blank=True)
    customer = models.ForeignKey(Profile, related_name='orders', on_delete=models.CASCADE, verbose_name='Клиент',)
    date = models.DateTimeField('Дата создания', auto_now_add=True)
    delivery_type = models.CharField('Тип доставки', max_length=20, blank=True)
    payment_type = models.CharField('Тип оплаты', db_index=True, max_length=50,)
    total_cost = models.DecimalField('Стоимость покупки', max_digits=10, decimal_places=2, default=0,)
    status = models.CharField('Статус заказа', db_index=True, max_length=20, default='new')
    order_number = models.CharField('Номер заказа', max_length=20, unique=True,)
    def __str__(self):
        return f'Order {self.order_number}'


class OrderItem(models.Model):
    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('catalog.Product', related_name='order_items', on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.count} x {self.product.price}'

