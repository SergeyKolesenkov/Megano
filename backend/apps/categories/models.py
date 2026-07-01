import re
from django.core.files.storage import default_storage
from django.db import models

def category_image_path(instance, filename):
    clean_title = re.sub(r'[^\w\s-]', '', instance.category.title).strip()
    clean_title = re.sub(r'[-\s]+', '-', clean_title)
    return f'categories/{clean_title}/{filename}'

def subcategory_image_path(instance, filename):
    clean_title = re.sub(r'[^\w\s-]', '', instance.subcategory.title).strip()
    clean_title = re.sub(r'[-\s]+', '-', clean_title)
    return f'subcategories/{clean_title}/{filename}'

class Category(models.Model):
    title = models.CharField('Название категории', max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Subcategory(models.Model):
    title = models.CharField('Подкатегория', max_length=50)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Родительская категория',
        related_name='subcategories'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

class CategoryImage(models.Model):
    category = models.ForeignKey(Category, related_name='images', on_delete=models.CASCADE, verbose_name="Категория товаров")
    src = models.ImageField('Ссылка на изображение', upload_to=category_image_path, max_length=500)
    alt = models.CharField('Альтернативный текст', max_length=200)

    class Meta:
        verbose_name = 'Изображение категории товара'
        verbose_name_plural = 'Изображения категорий товаров'

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_instance = CategoryImage.objects.get(pk=self.pk)
                if old_instance.src and old_instance.src != self.src:
                    if default_storage.exists(old_instance.src.name):
                        default_storage.delete(old_instance.src.name)
            except CategoryImage.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Изображение для {self.category.title}'

class SubcategoryImage(models.Model):
    subcategory = models.ForeignKey(Subcategory, related_name='images', on_delete=models.CASCADE, verbose_name="Подкатегория товаров")
    src = models.ImageField('Ссылка на изображение', upload_to=subcategory_image_path, max_length=100)
    alt = models.CharField('Альтернативный текст', max_length=200)

    class Meta:
        verbose_name = 'Изображение подкатегории товаров'
        verbose_name_plural = 'Изображения подкатегорий товаров'

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_instance = SubcategoryImage.objects.get(pk=self.pk)
                if old_instance.src and old_instance.src != self.src:
                    if default_storage.exists(old_instance.src.name):
                        default_storage.delete(old_instance.src.name)
            except SubcategoryImage.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Изображение для {self.subcategory.title}"