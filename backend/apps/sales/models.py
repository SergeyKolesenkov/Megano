from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from datetime import timezone

from apps.catalog.models import Product


class Sale(models.Model):
    class Meta:
        ordering = ['date_to']
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    product = models.ForeignKey( Product, on_delete=models.CASCADE, verbose_name='Товар')
    original_price = models.DecimalField('Исходная цена товара', max_digits=10, decimal_places=2)
    sale_price = models.DecimalField('Цена со скидкой', max_digits=10, decimal_places=2, db_index=True, validators=[MinValueValidator(0)])
    date_from = models.DateTimeField('Дата создания', auto_now_add=True, db_index=True)
    date_to = models.DateTimeField('Дата окончания', db_index=True, default=None, blank=True)
    is_active = models.BooleanField('Активна', db_index=True, default=True, blank=True)
    discount_type = models.CharField('Тип скидки', max_length=10, choices=[('percent', 'Процентная'), ('fixed', 'Фиксированная')])

    def __str__(self):
        try:
            return f'Скидка на {self.product.title}: {self.sale_price} руб.'
        except AttributeError:
            return 'Скидка без привязанного товара'

    @property
    def is_current(self):
        now = timezone.now()
        return (self.is_active and
                self.date_from <= now and
                (self.date_to is None or self.date_to >= now))

class SaleProduct(models.Model):
    class Meta:
        ordering = ['id']
        verbose_name = 'Скидка на продукт'
        verbose_name_plural = 'Скидки на продукты'
        unique_together = ['product', 'sale']

    product = models.ForeignKey('catalog.Product', related_name='sales', on_delete=models.CASCADE, null=True, verbose_name='Продукт')
    sale = models.ForeignKey('Sale', related_name='products', on_delete=models.CASCADE, verbose_name='Скидка')

    def __str__(self):
        return f"{self.product.title} - {self.sale.sale_price}"

    def clean(self):
        if self.sale and self.sale.is_active:
            active_sales = SaleProduct.objects.filter(
                product=self.product,
                sale__is_active=True
            ).exclude(pk=self.pk)

            if active_sales.exists():
                raise ValidationError(
                    'У товара может быть только одна скидка'
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
