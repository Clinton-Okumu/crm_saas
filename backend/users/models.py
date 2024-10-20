from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', _('Admin')
        MANAGER = 'manager', _('Manager')
        CLIENT = 'client', _('Client')

    email = models.EmailField(_('email address'), unique=True)
    company = models.CharField(_('company'), max_length=100, blank=True)
    role = models.CharField(
        _('role'),
        max_length=20,
        choices=Role.choices,
        default=Role.CLIENT
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'company', 'role']

    def save(self, *args, **kwargs):
        self.email = self.email.lower()  # Ensure email is case-insensitive
        try:
            validate_email(self.email)
        except ValidationError as e:
            raise ValueError(f"Invalid email format: {e}")
        super(CustomUser, self).save(*args, **kwargs)
        UserProfile.objects.get_or_create(user=self)  # Automatically create profile

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(_('bio'), blank=True)
    phone = models.CharField(_('phone'), max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.email}'s profile"
