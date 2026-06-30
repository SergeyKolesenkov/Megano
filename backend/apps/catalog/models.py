import re
from django.db import models
from apps.reviews.models import Review
from apps.tags.models import Tag
from django.core.files.storage import default_storage
from apps.categories.models import Category, Subcategory


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категория')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Подкатегория')
    title = models.CharField('Название товара', max_length=200)
    description = models.TextField('Краткое описание', blank=True)
    fullDescription = models.TextField('Полное описание', blank=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField('Количество на складе', default=0)
    freeDelivery = models.BooleanField('Бесплатная доставка', default=True)
    rating = models.DecimalField('Рейтинг', max_digits=3, decimal_places=1, default=0.0, blank=True)
    date = models.DateTimeField('Дата добавления', auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Теги')
    sort_index = models.IntegerField(default=0)
    sales_count = models.IntegerField('Количество продаж', default=0)
    current_price = models.DecimalField('цена со скидкой', max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-date']



    def __str__(self):
        return self.title



def product_image_path(instance, filename):
    clean_title = re.sub(r'[^\w\s-]', '', instance.product.title).strip()
    clean_title = re.sub(r'[-\s]+', '-', clean_title)
    return f'products/{clean_title}/{filename}'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE, verbose_name="Товар")
    src = models.ImageField('Ссылка на изображение', upload_to=product_image_path, max_length=500)
    alt = models.CharField('Альтернативный текст', max_length=200)

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = ProductImage.objects.get(pk=self.pk)
            if old_instance.src and old_instance.src != self.src:
                if default_storage.exists(old_instance.src.name):
                    default_storage.delete(old_instance.src.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Изображение для {self.product.title}'

