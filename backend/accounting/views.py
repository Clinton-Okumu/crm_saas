from rest_framework import generics, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum

from .models import Account, Transaction, TransactionLine, Invoice, Payment
from .serializers import (
    AccountSerializer, TransactionSerializer, 
    TransactionLineSerializer, InvoiceSerializer, PaymentSerializer
)

# Account Views
class AccountListCreateView(generics.ListCreateAPIView):
    """
    List all accounts or create a new account.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['account_type', 'is_active', 'account_code', 'parent']
    search_fields = ['name', 'account_code', 'description']
    ordering_fields = ['account_code', 'name', 'current_balance']
    ordering = ['account_code']

class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an account.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        account = self.get_object()
        
        if TransactionLine.objects.filter(Account=account).exists():
            return Response(
                {"error": "Cannot delete account with existing transactions"},
                status=status.HTTP_400_BAD_REQUEST
            )
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Transaction Views
class TransactionListCreateView(generics.ListCreateAPIView):
    """
    List all transactions or create a new transaction.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'transaction_type', 'date']
    search_fields = ['reference_number', 'description']
    ordering_fields = ['date', 'total_amount']
    ordering = ['-date']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a transaction.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

# Invoice Views
class InvoiceListCreateView(generics.ListCreateAPIView):
    """
    List all invoices or create a new invoice.
    """
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'customer', 'issue_date', 'due_date']
    search_fields = ['invoice_number', 'customer__name']
    ordering_fields = ['issue_date', 'due_date', 'total_amount']
    ordering = ['-issue_date']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class InvoiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an invoice.
    """
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.save(updated_by=self.request.user)
        instance.check_if_overdue()  # Check for overdue status

class InvoiceActionView(generics.GenericAPIView):
    """
    Handle various invoice actions.
    """
    queryset = Invoice.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        invoice = self.get_object()
        action = request.data.get('action')

        if action == 'mark_sent':
            invoice.mark_as_sent()
        elif action == 'mark_paid':
            invoice.mark_as_paid()
        else:
            return Response(
                {"error": "Invalid action"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"status": "success"})

# Payment Views
class PaymentListCreateView(generics.ListCreateAPIView):
    """
    List all payments or create a new payment.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['payment_method', 'payment_date', 'invoice']
    search_fields = ['reference_number', 'notes']
    ordering_fields = ['payment_date', 'amount']
    ordering = ['-payment_date']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a payment.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)