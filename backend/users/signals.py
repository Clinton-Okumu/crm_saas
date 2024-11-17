from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserProfile
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a UserProfile only if it doesn't already exist.
    """
    if created:
        try:
            if not hasattr(instance, 'profile'):  # Check if the profile already exists
                UserProfile.objects.create(user=instance)
                logger.info(f"UserProfile successfully created for {instance.email}.")
            else:
                logger.warning(f"UserProfile already exists for user {instance.id} ({instance.email}).")
        except Exception as e:
            logger.error(f"Failed to create UserProfile for {instance.email}: {e}")
