from django.urls import path
from .views import (
    AccountListCreateView,
    AccountDetailView,
    TransactionListCreateView,
    TransactionDetailView,
    InvoiceListCreateView,
    InvoiceDetailView,
    InvoiceActionView,
    PaymentListCreateView,
    PaymentDetailView,
)


app_name = "accounting"

urlpatterns = [
    # Account URLs
    path("accounts/", AccountListCreateView.as_view(), name="account-list"),
    path("accounts/<int:pk>/", AccountDetailView.as_view(), name="account-detail"),
    # Transaction URLs
    path("transactions/", TransactionListCreateView.as_view(), name="transaction-list"),
    path(
        "transactions/<int:pk>/",
        TransactionDetailView.as_view(),
        name="transaction-detail",
    ),
    # Invoice URLs
    path("invoices/", InvoiceListCreateView.as_view(), name="invoice-list"),
    path("invoices/<int:pk>/", InvoiceDetailView.as_view(), name="invoice-detail"),
    path(
        "invoices/<int:pk>/actions/", InvoiceActionView.as_view(), name="invoice-action"
    ),
    # Payment URLs
    path("payments/", PaymentListCreateView.as_view(), name="payment-list"),
    path("payments/<int:pk>/", PaymentDetailView.as_view(), name="payment-detail"),
]

