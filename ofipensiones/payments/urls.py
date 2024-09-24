from django.urls import path
from .views import PaymentReceiptList

urlpatterns = [
    path("payment_receipt/", PaymentReceiptList.as_view(), name="payment_receipt_list"),
]
