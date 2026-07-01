from django.contrib.auth.models import User
from django.db import models


class Review(models.Model):
    product = models.ForeignKey(
        'catalog.Product',
        null=True,
        blank=True,
        related_name='product_reviews',
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_authored', verbose_name='Автор')
    text = models.TextField('Текст отзыва', max_length=500)
    rate = models.IntegerField('Оценка', default=0, blank=True)
    date = models.DateTimeField('Дата отзыва', auto_now_add=True)
    updated = models.DateTimeField('Дата обновления', auto_now=True)
    email = models.EmailField('Электронная почта(Email)', blank=True)
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-date']

    def __str__(self):
        # return f"Отзыв от {self.author} на {self.product.title}"
        return str(self.rate)