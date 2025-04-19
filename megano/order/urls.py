from django.urls import path

from .views import OrderView, OrderByIdView

app_name = "order"

urlpatterns = [
    path("orders", OrderView.as_view(), name="orders"),
    path("order/<int:pk>", OrderByIdView.as_view(), name="orders_by_id"),
]
