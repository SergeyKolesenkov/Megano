from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum

from apps.catalog.models import Product


class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def count(self):
        return self.basket_items.aggregate(total=Sum('quantity'))['total'] or 0


    def get_total_price(self):
        return self.basket_items.aggregate(total=Sum('product__price',
                                                     field=F('product__price') * F('quantity')))['total'] or 0


class BasketItem(models.Model):
    id = models.AutoField(primary_key=True)
    basket = models.ForeignKey(Basket, related_name='basket_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
