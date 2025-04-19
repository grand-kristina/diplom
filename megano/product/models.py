from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator



class Specification(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Спецификация"
        verbose_name_plural = "Спецификации"


class Review(models.Model):
    author = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="author_review"
    )
    text = models.TextField()
    rate = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(
        "product.ProductShort", on_delete=models.CASCADE, related_name="product_reviews"
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class ProductShort(models.Model):
    category = models.ForeignKey(
        "catalog.CatalogItem", on_delete=models.CASCADE, null=False
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, validators=[MinValueValidator(0)]
    )
    count = models.IntegerField(null=False)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(null=False, max_length=100)
    description = models.TextField(null=True, blank=True)
    freeDelivery = models.BooleanField(default=False)
    images = models.ManyToManyField(
        "myauth.Avatar",
        blank=True,
        related_name="product_image",
    )
    tags = models.ManyToManyField("tags.Tag", blank=True, related_name="product_tag")
    reviews = models.ManyToManyField(
        "product.Review", blank=True, related_name="product_reviews"
    )
    rating = models.ManyToManyField(
        "product.Review", blank=True, related_name="product_rating"
    )
    specifications = models.ManyToManyField("product.Specification", blank=True)
    is_limited = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class SaleItem(models.Model):
    price = models.OneToOneField(
        ProductShort, on_delete=models.CASCADE, related_name="sale_price"
    )
    salePrice = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    date_from = models.DateField(null=True, blank=True)
    date_to = models.DateField(null=True, blank=True)
    title = models.ForeignKey(
        "product.ProductShort", on_delete=models.CASCADE, related_name="product_sale"
    )
    images = models.ManyToManyField(
        "myauth.Avatar",
        blank=True,
        related_name="sale_image",
    )

    class Meta:
        verbose_name = "Акционный товар"
        verbose_name_plural = "Акционные товары"
