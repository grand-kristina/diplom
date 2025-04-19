from django.db import models
from django.contrib.auth.models import User

from product.models import ProductShort


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductShort, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
