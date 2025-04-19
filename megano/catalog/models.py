from django.db import models

from myauth.models import Avatar


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

    def __str__(self):
        parent_title = self.parent.title if self.parent else ''
        return f'{self.title} - {parent_title}'
