import random

from rest_framework.views import APIView
from django.db.models import Q, Avg
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from .models import CatalogItem
from .serializers import CategoriesSerializer, CatalogSerializer, SaleSerializer
from product.models import ProductShort, SaleItem


class CategoriesView(APIView):
    def get(self, request: Request):
        root_categories = CatalogItem.objects.filter(parent__isnull=True)
        serializer = CategoriesSerializer(root_categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CatalogView(APIView):
    def get(self, request: Request) -> Response:
        name_filter = request.query_params.get("filter[name]", "").strip()
        min_price = request.query_params.get("filter[minPrice]", 0)
        max_price = request.query_params.get("filter[maxPrice]", 50000)
        free_delivery = (
            request.query_params.get("filter[freeDelivery]", "false").lower() == "true"
        )
        available = (
            request.query_params.get("filter[available]", "true").lower() == "true"
        )
        current_page = int(request.query_params.get("currentPage", 1))
        sort = request.query_params.get("sort", "price")
        sort_type = request.query_params.get("sortType", "inc")
        limit = int(request.query_params.get("limit", 20))

        filters = Q()
        if name_filter:
            filters &= Q(title__icontains=name_filter)
        if min_price and max_price:
            filters &= Q(price__gte=min_price, price__lte=max_price)
        if free_delivery:
            filters &= Q(freeDelivery=True)
        if available:
            filters &= Q(count__gt=0)

        order_by = sort if sort_type == "inc" else f"-{sort}"

        offset = (current_page - 1) * limit
        products = ProductShort.objects.filter(filters).order_by(order_by)
        paginated_products = products[offset : offset + limit]

        serializer = CatalogSerializer(paginated_products, many=True)

        response_data = {
            "items": serializer.data,
            "currentPage": current_page,
            "lastPage": (products.count() + limit - 1) // limit,
        }
        return Response(response_data, status=status.HTTP_200_OK)


class ProductPopularView(APIView):
    def get(self, request: Request) -> Response:
        products = (
            ProductShort.objects.annotate(avg_rating=Avg("reviews__rate"))
            .prefetch_related("images", "tags", "reviews", "specifications")
            .order_by("-avg_rating")
        )
        serializer = CatalogSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductLimitedView(APIView):
    def get(self, request: Request) -> Response:
        products = ProductShort.objects.prefetch_related(
            "images", "tags", "reviews", "rating", "specifications"
        ).filter(is_limited=True)
        serializer = CatalogSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SalesView(APIView):
    def get(self, request: Request) -> Response:
        current_page = int(request.query_params.get("currentPage", 1))
        page_size = 10
        offset = (current_page - 1) * page_size
        sales = SaleItem.objects.all()
        paginated_sales = sales[offset : offset + page_size]
        serializer = SaleSerializer(paginated_sales, many=True)
        response_data = {
            "items": serializer.data,
            "currentPage": current_page,
            "lastPage": (sales.count() + page_size - 1) // page_size,
        }
        return Response(response_data, status=status.HTTP_200_OK)


class BannersView(APIView):
    def get(self, request: Request) -> Response:
        product_ids = list(ProductShort.objects.values_list("id", flat=True))

        total_products = len(product_ids)
        if total_products > 0:
            random_ids = random.sample(product_ids, min(3, total_products))
        else:
            random_ids = []

        products = ProductShort.objects.filter(id__in=random_ids)

        serializer = CatalogSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
