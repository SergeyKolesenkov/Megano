from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from vshop.settings import AVATAR_DOWNLOAD_PATH, DEFAULT_AVATAR_PATH


class Profile(models.Model):
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    user = models.OneToOneField(User, on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )

    fullName = models.CharField('Полное имя',max_length=128,blank=True, null=True)
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
    )

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return None

    def __str__(self):
        return f'Профиль {self.user.username}'

class Avatar(models.Model):
    class Meta:
        verbose_name = 'Аватар'
        verbose_name_plural = 'Аватары'

    src = models.ImageField('Ссылка', 'avatars/', default='avatars/')
    alt = models.CharField('Альтернативный текст', max_length=100,)

    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name='related_avatar',
        verbose_name='Профиль',
    )

    def __str__(self):
        return self.alt if self.alt else f'Аватар {self.profile.user.username}'