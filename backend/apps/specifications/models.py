from django.db import models

from apps.catalog.models import Product


class Specification(models.Model):
    product = models.ForeignKey(Product, related_name='specifications', on_delete=models.CASCADE, verbose_name="Товар")
    name = models.CharField('Название характеристики', max_length=100)
    value = models.CharField('Значение характеристики', max_length=100)

    class Meta:
        verbose_name = 'Характеристика товара'
        verbose_name_plural = 'Характеристики товаров'

    def __str__(self):
        return f'{self.name}: {self.value}'
