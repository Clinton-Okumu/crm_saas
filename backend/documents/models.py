from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
import uuid

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class Document(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archived', 'Archived')
    ]

    # Basic info
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    # File handling
    file = models.FileField(
        upload_to='documents/%Y/%m/%d/',
        validators=[FileExtensionValidator(
            ['pdf', 'doc', 'docx', 'txt', 'xls', 'xlsx']
        )]
    )
    file_size = models.BigIntegerField(editable=False, null=True)
    version = models.PositiveIntegerField(default=1)

    # Access control
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='documents_created'
    )
    shared_with = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='DocumentShare',
        related_name='shared_documents',
        through_fields=('document', 'user'),  # Specify through fields
        blank=True
    )
    is_public = models.BooleanField(default=False)

    # Remove project field for now - can add back when projects app exists
    # project = models.ForeignKey(
    #     'projects.Project',
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name='documents'
    # )

    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_accessed = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-updated_at']
        permissions = [
            ("can_archive_document", "Can archive document"),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{str(uuid.uuid4())[:8]}")
        
        if self.file and not self.file_size:
            self.file_size = self.file.size
            
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.file:
            self.file.delete(save=False)
        super().delete(*args, **kwargs)

class DocumentShare(models.Model):
    PERMISSION_CHOICES = [
        ('view', 'View Only'),
        ('edit', 'Edit')
    ]

    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    permission = models.CharField(
        max_length=10,
        choices=PERMISSION_CHOICES,
        default='view'
    )
    shared_at = models.DateTimeField(auto_now_add=True)
    shared_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='documents_shared'
    )

    class Meta:
        unique_together = ['document', 'user']

    def __str__(self):
        return f"{self.document.title} shared with {self.user}"
