from django.db import transaction
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import status

from .models import Basket
from product.models import ProductShort
from .serializers import BasketSerializers
from catalog.serializers import CatalogSerializer


class BasketView(APIView):
    def get(self, request: Request) -> Response:
        if request.user.is_authenticated:
            user_str = str(request.user.username)
            baskets = Basket.objects.select_related("product").filter(
                user__username=user_str
            )
            counts = {}
            unique_products = []
            for basket in baskets:
                product_id = basket.product.id
                if product_id in counts:
                    counts[product_id] += basket.count
                else:
                    counts[product_id] = basket.count
                    unique_products.append(basket.product)

            serializer = BasketSerializers(
                unique_products,
                many=True,
                context={"counts": counts},
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            basket = request.session.get("basket", {})
            product_ids = basket.keys()
            products = ProductShort.objects.filter(id__in=product_ids)
            counts = {int(product_id): count for product_id, count in basket.items()}

            serializer = BasketSerializers(
                products,
                many=True,
                context={"counts": counts},
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request: Request) -> Response:
        data = request.data
        product_id = data["id"]
        count = data["count"]

        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
            product = ProductShort.objects.get(id=product_id)
            basket, created = Basket.objects.get_or_create(
                user=user, product=product, defaults={"count": count}
            )
            if not created:
                basket.count += count
                basket.save()
        else:
            basket = request.session.get("basket", {})
            if product_id in basket:
                basket[product_id] += count
            else:
                basket[product_id] = count
            request.session["basket"] = basket

        return Response(status=status.HTTP_200_OK)

    @transaction.atomic
    def delete(self, request: Request) -> Response:
        product_id = request.data["id"]

        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
            basket = Basket.objects.filter(user=user, product_id=product_id)
            if basket:
                basket.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            basket = request.session.get("basket", {})
            if str(product_id) in basket:
                del basket[str(product_id)]
                request.session["basket"] = basket
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
