from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db import transaction
from rest_framework import permissions

from .models import ProductShort, Review
from .serializers import ProductSerializer, CreateReviewsSerializer, ReviewsSerializer


class ProductByIdView(APIView):
    def get(self, request: Request, pk: int) -> Response:
        product = (
            ProductShort.objects.prefetch_related(
                "images", "tags", "reviews", "rating", "specifications"
            )
            .filter(id=pk)
            .first()
        )
        if product:
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)


class CreateReviewByIdView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request: Request, pk: int):
        review_exists = Review.objects.filter(author=request.user, product=pk).exists()
        if not review_exists:
            product = ProductShort.objects.get(id=pk)
            data = request.data.copy()
            data["product"] = product.id
            data.pop("email")
            serializer = CreateReviewsSerializer(
                data=data, context={"request": request}
            )
            if serializer.is_valid():
                review = serializer.save()
                serializer_response = ReviewsSerializer(review)
                return Response(serializer_response.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
