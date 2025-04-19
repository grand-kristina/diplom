from django.contrib import admin

from .models import Avatar, Profile


@admin.register(Avatar)
class ImageAdmin(admin.ModelAdmin):
    list_display = "id", "src", "alt"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "fullName",
        "phone",
        "balance",
        "avatar",
    )
