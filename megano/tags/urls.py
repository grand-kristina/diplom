from django.urls import path

from .views import TagView

app_name = "tags"

urlpatterns = [
    path("tags/", TagView.as_view(), name="tags"),
]
