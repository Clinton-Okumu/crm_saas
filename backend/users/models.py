from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    """
    handles user roles and different access points across the system
    """
    objects = CustomUserManager()
    class Role(models.TextChoices):
        # System Roles
        SUPER_ADMIN = 'super_admin', _('Super Admin')
        
        # HR Module Roles
        HR_ADMIN = 'hr_admin', _('HR Admin')
        HR_MANAGER = 'hr_manager', _('HR Manager')
        HR_STAFF = 'hr_staff', _('HR Staff')
        
        # Accounting Module Roles
        ACCOUNTING_ADMIN = 'accounting_admin', _('Accounting Admin')
        ACCOUNTANT = 'accountant', _('Accountant')
        
        # Project Management Roles
        PROJECT_ADMIN = 'project_admin', _('Project Admin')
        PROJECT_MANAGER = 'project_manager', _('Project Manager')
        PROJECT_MEMBER = 'project_member', _('Project Member')
        
        # CRM Roles
        CRM_ADMIN = 'crm_admin', _('CRM Admin')
        CRM_MANAGER = 'crm_manager', _('CRM Manager')
        SALES_REP = 'sales_rep', _('Sales Representative')
        
        # Client Role
        CLIENT = 'client', _('Client')
        
    class Module(models.TextChoices):
        HRM = 'hrm', _('Human Resources')
        ACCOUNTING = 'accounting', _('Accounting')
        PROJECT = 'project', _('Project Management')
        CRM = 'crm', _('Customer Relationship')
        MEETING = 'meeting', _('Meeting Management')
    
    username = None
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _('A user with that email already exists.'),
        }
    )

    first_name = models.CharField(
        _('first name'),
        max_length=30,
        blank=False
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=False
    )
    
    company = models.CharField(
        _('company'),
        max_length=100,
        blank=True
    )
    
    role = models.CharField(
        _('role'),
        max_length=20,
        choices=Role.choices,
        default=Role.CLIENT
    )
    
    primary_module = models.CharField(
        _('primary module'),
        max_length=20,
        choices=Module.choices,
        null=True
    )
    
    accessible_modules = models.JSONField(
        _('accessible modules'),
        default=list,
        help_text=_('List of modules this user can access')
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether this user should be treated as active.')
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name','company', 'role']
    
    def __str__(self):
        return f"{self.email} - {self.get_role_display()}"
    
    def save(self, *args, **kwargs):
        # Ensure email is lowercase
        self.email = self.email.lower()
        
        # Validate email format
        validate_email(self.email)
        
        # Set primary module if not set
        if not self.primary_module:
            self.primary_module = self._get_default_module()
            
        # Set accessible modules if not set
        if not self.accessible_modules:
            self.accessible_modules = self._get_default_accessible_modules()
    
        super().save(*args, **kwargs)
    def _get_default_module(self):
        """
        Determines the default primary module based on user's role
        """
        role_module_mapping = {
            'hr_admin': self.Module.HRM,
            'hr_manager': self.Module.HRM,
            'hr_staff': self.Module.HRM,
            'accounting_admin': self.Module.ACCOUNTING,
            'accountant': self.Module.ACCOUNTING,
            'project_admin': self.Module.PROJECT,
            'project_manager': self.Module.PROJECT,
            'project_member': self.Module.PROJECT,
            'crm_admin': self.Module.CRM,
            'crm_manager': self.Module.CRM,
            'sales_rep': self.Module.CRM,
        }
        return role_module_mapping.get(self.role)

    def _get_default_accessible_modules(self):
        """
        Determines the default accessible modules based on user's role
        """
        if self.role == self.Role.SUPER_ADMIN:
            return [choice[0] for choice in self.Module.choices]
            
        role_access_mapping = {
            # HR roles
            'hr_admin': [self.Module.HRM, self.Module.MEETING],
            'hr_manager': [self.Module.HRM, self.Module.MEETING],
            'hr_staff': [self.Module.HRM],
            
            # Accounting roles
            'accounting_admin': [self.Module.ACCOUNTING],
            'accountant': [self.Module.ACCOUNTING],
            
            # Project roles
            'project_admin': [self.Module.PROJECT, self.Module.MEETING],
            'project_manager': [self.Module.PROJECT, self.Module.MEETING],
            'project_member': [self.Module.PROJECT],
            
            # CRM roles
            'crm_admin': [self.Module.CRM, self.Module.MEETING],
            'crm_manager': [self.Module.CRM, self.Module.MEETING],
            'sales_rep': [self.Module.CRM],
            
            # Client role
            'client': [self.Module.PROJECT]  # Clients only see their projects
        }
        return role_access_mapping.get(self.role, [])

    def has_module_access(self, module):
        """
        Check if user has access to a specific module
        """
        return module in self.accessible_modules

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['email']

class UserProfile(models.Model):
    """
    Extended profile information for users
    """
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    phone = models.CharField(
        _('phone number'),
        max_length=20,
        blank=True,
        default=""
    )
    department = models.CharField(
        _('department'),
        max_length=100,
        blank=True,
        default=""
    )
    position = models.CharField(
        _('position'),
        max_length=100,
        blank=True,
        default=""
    )
    bio = models.TextField(
        _('biography'),
        blank=True,
        default=""
    )
    date_of_birth = models.DateField(
        _('date of birth'),
        null=True,
        blank=True
    )

    def get_full_name(self):
        """
        Returns the user's full name.
        """
        return f"{self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return f"{self.user.email}'s profile"

    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')
        ordering = ['user__email']