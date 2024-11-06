from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from .models import CustomUser, UserProfile

class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom adapter for django-allauth to handle our CustomUser model
    """


    def populate_username(self, request, user):
        """
        Use email as username since we're using email authentication
        """
        user.username = user.email

    def is_open_for_signup(self, request):
        """
        Control whether signups are allowed
        """
        return getattr(settings, 'ACCOUNT_ALLOW_SIGNUPS', True)

    def get_signup_form_class(self):
        """
        Return custom signup form if you have one
        """
        return None  # Replace with your custom form if you create one

    def get_login_form_class(self):
        """
        Return custom login form if you have one
        """
        return None  # Replace with your custom form if you create one