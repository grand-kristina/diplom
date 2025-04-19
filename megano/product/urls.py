from django.urls import path

from .views import ProductByIdView, CreateReviewByIdView


app_name = "product"

urlpatterns = [
    path("product/<int:pk>", ProductByIdView.as_view(), name="product_by_id"),
    path(
        "product/<int:pk>/reviews",
        CreateReviewByIdView.as_view(),
        name="product_review_by_id",
    ),
]
