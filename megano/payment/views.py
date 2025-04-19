from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from django.db import transaction

from .tasks import validation_cart_number
from .models import Payment
from order.models import Order


class PaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request: Request, pk: int) -> Response:
        try:
            data = request.data
            task = validation_cart_number(data["number"])
            if task:
                order = Order.objects.get(id=pk)
                Payment.objects.create(
                    order=order,
                    number=data["number"],
                    name=data["name"],
                    month=data["month"],
                    year=data["year"],
                    code=data["code"],
                )
                order.status = "accepted"
                order.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
