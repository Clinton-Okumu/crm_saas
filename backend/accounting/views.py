from rest_framework import generics, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Account, Transaction, Invoice, Payment
from .serializers import (
    AccountSerializer,
    TransactionSerializer,
    InvoiceSerializer,
    PaymentSerializer,
)
from .permissions import (
    CanManageAccounts,
    CanManageTransactions,
    CanManageInvoices,
    CanManagePayments,
)


# Account Views
class AccountListCreateView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [CanManageAccounts]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["account_type", "is_active", "account_code", "parent"]
    search_fields = ["name", "account_code", "description"]
    ordering_fields = ["account_code", "name", "current_balance"]
    ordering = ["account_code"]


class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [CanManageAccounts]

    def destroy(self, request, *args, **kwargs):
        account = self.get_object()
        if TransactionLine.objects.filter(Account=account).exists():
            return Response(
                {"error": "Cannot delete account with existing transactions"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Transaction Views
class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [CanManageTransactions]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "transaction_type", "date"]
    search_fields = ["reference_number", "description"]
    ordering_fields = ["date", "total_amount"]
    ordering = ["-date"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [CanManageTransactions]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


# Invoice Views
class InvoiceListCreateView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [CanManageInvoices]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "customer", "issue_date", "due_date"]
    search_fields = ["invoice_number", "customer__name"]
    ordering_fields = ["issue_date", "due_date", "total_amount"]
    ordering = ["-issue_date"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class InvoiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [CanManageInvoices]

    def perform_update(self, serializer):
        instance = serializer.save(updated_by=self.request.user)
        instance.check_if_overdue()


class InvoiceActionView(generics.GenericAPIView):
    queryset = Invoice.objects.all()
    permission_classes = [CanManageInvoices]

    def post(self, request, *args, **kwargs):
        invoice = self.get_object()
        action = request.data.get("action")

        if action == "mark_sent":
            invoice.mark_as_sent()
        elif action == "mark_paid":
            invoice.mark_as_paid()
        else:
            return Response(
                {"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"status": "success"})


# Payment Views
class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [CanManagePayments]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["payment_method", "payment_date", "invoice"]
    search_fields = ["reference_number", "notes"]
    ordering_fields = ["payment_date", "amount"]
    ordering = ["-payment_date"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [CanManagePayments]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
