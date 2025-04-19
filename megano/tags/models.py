from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"
