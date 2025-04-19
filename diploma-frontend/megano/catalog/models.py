from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from myauth.models import Avatar, Profile


class CatalogItem(models.Model):
    title = models.CharField(max_length=255)
    image = models.ForeignKey(Avatar, on_delete=models.SET_NULL, null=True, blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategories",
    )

    class Meta:
        verbose_name = "Каталог"
        verbose_name_plural = "Каталог"
