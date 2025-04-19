from django.db import models
from django.contrib.auth.models import User


class Avatar(models.Model):
    src = models.ImageField(
        upload_to="app_users/avatars/user_avatars/",
        default="app_users/avatars/default.png",
        null=True,
        blank=True,
        verbose_name="Ссылка",
    )
    alt = models.CharField(
        max_length=128, null=True, blank=True, verbose_name="Описание"
    )

    class Meta:
        verbose_name = "Аватар"
        verbose_name_plural = "Аватары"
    
    def __str__(self):
        return f'{self.alt}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    fullName = models.CharField(max_length=128, verbose_name="Полное имя")
    phone = models.PositiveIntegerField(
        blank=True, null=True, unique=True, verbose_name="Номер телефона"
    )
    balance = models.DecimalField(
        decimal_places=2, max_digits=10, default=0, verbose_name="Баланс"
    )
    avatar = models.ForeignKey(
        Avatar,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="profile",
        verbose_name="Аватар",
    )

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
