from datetime import date
from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError

ASSET_CODE_RANGE = "1"
LIABILITY_CODE_RANGE = "2"
EQUITY_CODE_RANGE = "3"
INCOME_CODE_RANGE = "4"
EXPENSE_CODE_RANGE = "5"


ACCOUNT_TYPES = (
    ("asset", "Asset"),
    ("liability", "Liability"),
    ("equity", "Equity"),
    ("income", "Income"),
    ("expense", "Expense"),
)


class Account(models.Model):
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    account_code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    current_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["account_code"]
        unique_together = ["parent", "name"]

    def __str__(self):
        return f"{self.account_code} - {self.name}"


TRANSACTION_STATUS = (
    ("draft", "Draft"),
    ("posted", "Posted"),
    ("void", "Void"),
)

TRANSACTION_TYPES = (
    ("invoice", "Invoice"),
    ("payment", "Payment"),
    ("expense", "Expense"),
    ("journal", "Journal Entry"),
)


class Transaction(models.Model):
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    reference_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(
        max_length=20, choices=TRANSACTION_STATUS, default="draft"
    )
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    total_amount = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("users.CustomUser", on_delete=models.PROTECT)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.reference_number} - {self.description} ({self.total_amount})"


class TransactionLine(models.Model):
    transaction = models.ForeignKey(
        Transaction, on_delete=models.CASCADE, related_name="lines"
    )
    Account = models.ForeignKey(Account, on_delete=models.PROTECT)

    # Either debit or credit will be filled, the other will be zero
    debit_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    credit_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"self.account.name : Dr {self.debit_amount}  Cr {self.credit_amount}"

    def clean(self):
        # Validation to ensure either debit or credit is filled, but not both
        if self.debit_amount > 0 and self.credit_amount > 0:
            raise ValidationError("A line cannot have both debit and credit amounts")
        if self.debit_amount == 0 and self.credit_amount == 0:
            raise ValidationError(
                "Either debit or credit amount must be greater than zero"
            )

    @property
    def amount(self):
        """Returns the non-zero amount (whether it's debit or credit)"""
        return self.debit_amount or self.credit_amount


INVOICE_STATUS = (
    ("draft", "Draft"),  # Invoice created but not sent
    ("sent", "Sent"),  # Invoice sent to customer
    ("paid", "Paid"),  # Invoice has been paid
    ("overdue", "Overdue"),  # Payment deadline passed
    ("void", "Void"),  # Invoice cancelled/voided
)


class Invoice(models.Model):
    # Relationships
    customer = models.ForeignKey("crm.Customer", on_delete=models.PROTECT)

    # Invoice Details
    invoice_number = models.CharField(max_length=50, unique=True)
    issue_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=INVOICE_STATUS, default="draft")

    # Financial Details
    subtotal = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    # Additional Information
    terms_and_conditions = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("users.CustomUser", on_delete=models.PROTECT)

    class Meta:
        ordering = ["-issue_date", "-invoice_number"]

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.customer.name}"

    def clean(self):
        # Validate due date is after issue date
        if self.due_date < self.issue_date:
            raise ValidationError("Due date cannot be before issue date")

    def calculate_totals(self):
        """Calculate invoice totals from line items"""
        self.subtotal = sum(line.total for line in self.lines.all())
        # Assuming standard tax rate, could be made more complex
        self.tax = self.subtotal * Decimal("0.15")  # 15% tax
        self.total_amount = self.subtotal + self.tax

    def mark_as_sent(self):
        """Mark invoice as sent"""
        if self.status == "draft":
            self.status = "sent"
            self.save()

    def mark_as_paid(self):
        """Mark invoice as paid"""
        if self.status in ["sent", "overdue"]:
            self.status = "paid"
            self.save()

    def check_if_overdue(self):
        """Check and update overdue status"""
        if self.status == "sent" and self.due_date < date.today():
            self.status = "overdue"
            self.save()


PAYMENT_METHODS = (
    ("cash", "Cash"),
    ("bank_transfer", "Bank Transfer"),
    ("credit_card", "Credit Card"),
    ("check", "Check"),
    ("mobile_money", "Mobile Money"),
    ("other", "Other"),
)


class Payment(models.Model):
    # Relationship
    invoice = models.ForeignKey(
        "Invoice", on_delete=models.PROTECT, related_name="payments"
    )

    # Payment Details
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    reference_number = models.CharField(max_length=50, unique=True)

    # Additional Information
    notes = models.TextField(blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("users.CustomUser", on_delete=models.PROTECT)

    class Meta:
        ordering = ["-payment_date", "-created_at"]

    def __str__(self):
        return f"Payment {self.reference_number} - {self.amount} for Invoice {self.invoice.invoice_number}"

    def clean(self):
        # Validate payment amount doesn't exceed invoice remaining balance
        total_payments = (
            self.invoice.payments.aggregate(total=models.Sum("amount"))["total"] or 0
        )
        if self.id:  # If payment exists, exclude it from total
            total_payments -= Payment.objects.get(id=self.id).amount

        if (total_payments + self.amount) > self.invoice.total_amount:
            raise ValidationError("Total payments cannot exceed invoice amount")

    def save(self, *args, **kwargs):
        # Check if invoice should be marked as paid
        super().save(*args, **kwargs)
        total_payments = (
            self.invoice.payments.aggregate(total=models.Sum("amount"))["total"] or 0
        )

        if total_payments >= self.invoice.total_amount:
            self.invoice.mark_as_paid()

