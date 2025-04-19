from rest_framework import serializers

from .models import Order
from product.serializers import ProductSerializer
from myauth.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fileds = [
            "fullName",
            "email",
            "phone",
        ]


class OrderSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(source="profile.fullName")
    email = serializers.CharField(source="profile.user.email")
    phone = serializers.CharField(source="profile.phone")
    products = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "createdAt",
            "fullName",
            "email",
            "phone",
            "deliveryType",
            "paymentType",
            "totalCost",
            "status",
            "city",
            "address",
            "products",
        ]

    def get_products(self, obj):
        products_data = ProductSerializer(obj.products.all(), many=True).data

        for product in products_data:
            product["count"] = obj.totalCount

        return products_data
