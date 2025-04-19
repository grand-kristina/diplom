from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CatalogItem
from myauth.models import Avatar
from .forms import CustomUserCreationAdminForm


@admin.register(CatalogItem)
class CatalogItemAdmin(admin.ModelAdmin):
    list_display = "title", "image", "parent"
