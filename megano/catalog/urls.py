from django.urls import path

from .views import (
    CategoriesView,
    CatalogView,
    ProductPopularView,
    ProductLimitedView,
    SalesView,
    BannersView,
)

app_name = "catalog"

urlpatterns = [
    path("categories/", CategoriesView.as_view(), name="categories"),
    path("catalog/", CatalogView.as_view(), name="catalog"),
    path("products/popular/", ProductPopularView.as_view(), name="popular_products"),
    path("products/limited/", ProductLimitedView.as_view(), name="limited_products"),
    path("sales/", SalesView.as_view(), name="sales"),
    path("banners/", BannersView.as_view(), name="banners"),
]
