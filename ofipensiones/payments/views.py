from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import OfipensionesLog, TermPayment
from .serializers import PaymentReceiptSerializer

import time
from datetime import timedelta


class PaymentReceiptList(APIView):
    def get(self, request):
        s = time.time()
        payment_receipts = TermPayment.objects.all()
        serializer = PaymentReceiptSerializer(payment_receipts, many=True)
        e = time.time()

        delta = timedelta(seconds=e - s)

        OfipensionesLog(operation_name="payment_receipts", time_taken=delta).save()

        return Response(serializer.data, status=status.HTTP_200_OK)
