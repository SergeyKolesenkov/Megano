from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    user = models.OneToOneField(User, on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )

    # full_name = models.CharField('Полное имя',max_length=128,blank=True, null=True)
    phone = models.CharField('Телефон',max_length=20,blank=True,null=True,)
    email = models.EmailField('Электронная почта', blank=True, null=True,)
    date = models.DateTimeField('Дата создания', auto_now_add=True,)
    updated = models.DateTimeField('Дата обновления', auto_now=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])],
        help_text="Аватар пользователя"
    )
    def __str__(self):
        return f"Профиль {self.user.username}"
