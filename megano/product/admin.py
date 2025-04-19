from django.contrib import admin

from .models import ProductShort, Review, SaleItem, Specification


class ReviewInLine(admin.TabularInline):
    model = Review
    readonly_fields = ("date", "author", "text", "rate")
    extra = 1


@admin.register(ProductShort)
class ProductShortAdmin(admin.ModelAdmin):
    inlines = [ReviewInLine]
    list_display = (
        "category",
        "price",
        "count",
        "date",
        "title",
        "description",
        "freeDelivery",
        "is_limited",
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "text",
        "rate",
        "product",
    )
    readonly_fields = ("date",)


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = (
        "price",
        "salePrice",
        "date_from",
        "date_to",
    )


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "value",
    )
