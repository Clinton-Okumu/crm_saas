from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Customer(models.Model):
    """
    Represents a customer or potential customer in the CRM system.
    
    This model stores basic information about companies/customers, including
    their contact details, current status in the sales pipeline, and address
    information.
    """
    
    # Contact Information
    name = models.CharField(
        max_length=200,
        help_text="Company or customer name"
    )
    email = models.EmailField(
        blank=True,
        help_text="Primary email address for the customer"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Primary phone number"
    )
    website = models.URLField(
        blank=True,
        help_text="Company website URL"
    )
    
    # Location Information
    address = models.TextField(
        blank=True,
        help_text="Complete address of the customer"
    )
    
    # Status and Classification
    STATUS_CHOICES = [
        ('lead', 'Lead'),           # Potential customer, initial contact
        ('customer', 'Customer'),    # Active customer
        ('inactive', 'Inactive')     # Former or inactive customer
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='lead',
        help_text="Current status of the customer in the sales pipeline"
    )
    
    # Record Keeping
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the customer was added"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date and time of the last update"
    )

    def __str__(self):
        """Returns the string representation of the customer."""
        return self.name

class Contact(models.Model):
    """
    Represents an individual contact person associated with a customer.
    
    This model stores information about specific individuals within a customer
    organization, including their personal contact details and role.
    """
    
    # Relationship
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        help_text="The customer/company this contact belongs to"
    )
    
    # Personal Information
    first_name = models.CharField(
        max_length=100,
        help_text="Contact's first name"
    )
    last_name = models.CharField(
        max_length=100,
        help_text="Contact's last name"
    )
    email = models.EmailField(
        blank=True,
        help_text="Contact's email address"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Contact's phone number"
    )
    position = models.CharField(
        max_length=100,
        blank=True,
        help_text="Contact's job title or position"
    )
    
    # Status and Metadata
    is_primary = models.BooleanField(
        default=False,
        help_text="Indicates if this is the primary contact for the customer"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the contact was added"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date and time of the last update"
    )

    def __str__(self):
        """Returns the full name of the contact."""
        return f"{self.first_name} {self.last_name}"

class Interaction(models.Model):
    """
    Tracks all interactions with customers and their contacts.
    
    This model records various types of communications and interactions
    with customers, including calls, emails, meetings, and notes. Each
    interaction can be linked to both a customer and optionally a
    specific contact person.
    """
    
    # Relationships
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        help_text="The customer involved in this interaction"
    )
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="The specific contact person involved (if any)"
    )
    
    # Interaction Details
    TYPE_CHOICES = [
        ('call', 'Phone Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
        ('note', 'Note') 
    ]
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        help_text="The type of interaction"
    )
    notes = models.TextField(
        help_text="Detailed notes about the interaction"
    )
    date = models.DateTimeField(
        help_text="Date and time of the interaction"
    )
    
    # Record Keeping
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when this record was created"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Instead of User
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_interactions',  # Add related_name
        help_text="User who recorded this interaction"
    )

    def __str__(self):
        """Returns a description of the interaction."""
        return f"{self.type} with {self.customer.name} on {self.date.date()}"
