from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from rest_framework import permissions

from .serializers import OrderSerializer
from .models import Order
from myauth.models import Profile
from basket.models import Basket

from product.models import ProductShort


class OrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        user = request.user
        orders = Order.objects.filter(profile__user=user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request: Request) -> Response:
        data = request.data
        product_obj = []
        count = 0
        profile = Profile.objects.filter(user=request.user).first()
        for product in data:
            prod = ProductShort.objects.prefetch_related(
                "images", "tags", "reviews", "rating", "specifications"
            ).get(id=product["id"])
            product_obj.append(prod)
            count += product["count"]
        order = Order.objects.create(
            profile=profile,
            totalCost=count * float(product["price"]),
            totalCount=count,
        )
        order.products.set(product_obj)
        return Response({"orderId": order.id}, status=status.HTTP_200_OK)


class OrderByIdView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, pk: int) -> Response:
        order = Order.objects.filter(id=pk).first()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request: Request, pk: int) -> Response:
        data = request.data

        order = Order.objects.get(id=pk, profile__user=request.user)

        order.city = data.get("city", order.city)
        order.address = data.get("address", order.address)
        order.paymentType = data.get("paymentType", order.paymentType) or "another card"
        order.deliveryType = data.get("deliveryType", order.deliveryType) or "standard"
        order.status = data.get("status", order.status) or "new"

        basket = data.get("basket", {})
        if basket:
            product_ids = [int(product_id) for product_id in basket.keys()]
            products = ProductShort.objects.filter(id__in=product_ids)
            order.products.set(products)

        order.save()

        Basket.objects.filter(user=request.user).delete()

        return Response({"orderId": order.id}, status=status.HTTP_200_OK)
