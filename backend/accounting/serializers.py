from django.db import models
from rest_framework import serializers
from .models import Account, Transaction, TransactionLine, Invoice, Payment

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'id', 'name', 'account_type', 'account_code', 
            'description', 'parent', 'is_active', 
            'current_balance', 'created_at', 'updated_at'
        ]

class TransactionLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionLine
        fields = [
            'id', 'transaction', 'Account',
            'debit_amount', 'credit_amount',
            'created_at', 'updated_at', 'amount'
        ]
        read_only_fields = ['created_at', 'updated_at']

class TransactionSerializer(serializers.ModelSerializer):
    lines = TransactionLineSerializer(many=True, read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'date', 'description', 'reference_number',
            'status', 'transaction_type', 'total_amount',
            'created_at', 'updated_at', 'created_by', 'lines'
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by']

    def create(self, validated_data):
        lines_data = self.context.get('lines', [])
        transaction = Transaction.objects.create(**validated_data)
        
        for line_data in lines_data:
            TransactionLine.objects.create(transaction=transaction, **line_data)
        
        return transaction

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [
            'id', 'customer', 'invoice_number', 'issue_date',
            'due_date', 'status', 'subtotal', 'tax',
            'total_amount', 'terms_and_conditions', 'notes',
            'created_at', 'updated_at', 'created_by'
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by']

    def validate(self, data):
        """
        Check that due date is after issue date
        """
        if data['due_date'] < data['issue_date']:
            raise serializers.ValidationError({
                "due_date": "Due date must be after issue date"
            })
        return data

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id', 'invoice', 'payment_date', 'payment_method',
            'amount', 'reference_number', 'notes',
            'created_at', 'updated_at', 'created_by'
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by']

    def validate(self, data):
        """
        Check that payment amount doesn't exceed remaining balance
        """
        invoice = data['invoice']
        total_payments = invoice.payments.aggregate(
            total=models.Sum('amount'))['total'] or 0
            
        if self.instance:  # If updating existing payment
            total_payments -= self.instance.amount
            
        if (total_payments + data['amount']) > invoice.total_amount:
            raise serializers.ValidationError({
                "amount": "Total payments cannot exceed invoice amount"
            })
        return data
