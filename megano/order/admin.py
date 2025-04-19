from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "createdAt",
        "get_profile_fullName",
        "get_profile_email",
        "get_profile_phone",
        "deliveryType",
        "paymentType",
        "totalCost",
        "totalCount",
        "status",
        "city",
        "address",
        "get_products",
    )

    def get_profile_fullName(self, obj):
        return obj.profile.fullName

    get_profile_fullName.short_description = "Полное имя"

    def get_profile_email(self, obj):
        return obj.profile.user.email

    get_profile_email.short_description = "Email"

    def get_profile_phone(self, obj):
        return obj.profile.phone

    get_profile_phone.short_description = "Телефон"

    def get_products(self, obj):
        return ", ".join([product.title for product in obj.products.all()])

    get_products.short_description = "Товары"
