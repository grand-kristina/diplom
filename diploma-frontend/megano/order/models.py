from django.core.validators import MinValueValidator
from django.db import models

from myauth.models import Profile
from catalog.models import CatalogItem
from myauth.models import Avatar
from tags.models import Tag
from product.models import ProductShort


class Order(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="order_profile"
    )
    deliveryType = models.CharField(max_length=100, null=True, blank=True)
    paymentType = models.CharField(max_length=100, null=True, blank=True)
    totalCost = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    totalCount = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], null=True, blank=True
    )
    status = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    products = models.ManyToManyField(ProductShort, related_name="order_products")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
