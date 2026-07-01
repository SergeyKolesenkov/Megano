from django.db import models

class Tag(models.Model):
    name = models.CharField('Название тега', max_length=20)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
