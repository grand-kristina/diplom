from django.db import models

from order.models import Order


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    number = models.CharField(max_length=16, db_index=True)
    name = models.CharField(max_length=255)
    month = models.CharField(max_length=2)
    year = models.CharField(max_length=4)
    code = models.CharField(max_length=3)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
