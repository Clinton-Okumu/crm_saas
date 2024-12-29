from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator

class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(
        upload_to='documents/',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'txt'])]
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


