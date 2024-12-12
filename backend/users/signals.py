from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser, UserProfile
from hrm.models import Employee, Department, Position
import logging
from datetime import date

logger = logging.getLogger(__name__)

@receiver(post_save, sender=CustomUser)
def create_user_profile_and_employee(sender, instance, created, **kwargs):
    """
    Create a UserProfile and an Employee record (if applicable) when a CustomUser is created.
    """
    if created:
        logger.info(f"Creating profile and employee for {instance.email}...")

        try:
            # Create UserProfile
            if not hasattr(instance, 'profile'):
                UserProfile.objects.create(user=instance)
                logger.info(f"UserProfile successfully created for {instance.email}.")
            else:
                logger.warning(f"UserProfile already exists for user {instance.id} ({instance.email}).")

            # Create Employee record for all users except clients
            if instance.role != CustomUser.Role.CLIENT:
                # Define your default department and position
                default_department = Department.objects.first()
                default_position = Position.objects.first()

                if default_department and default_position:
                    logger.info(f"Creating Employee record for {instance.email}...")

                    # Create the Employee record
                    Employee.objects.create(
                        first_name=instance.first_name,
                        last_name=instance.last_name,
                        email=instance.email,
                        phone=instance.phone,
                        employee_id=f"EMP{instance.id:05d}",
                        department=default_department,
                        position=default_position,
                        hire_date=date.today(),
                        is_active=True,  # Defaulting to True as per your model definition
                        date_of_birth=None,  # You can adjust this based on your user input or leave it as None
                    )
                    logger.info(f"Employee {instance.email} created successfully.")
                else:
                    logger.error(f"Error: Default department or position not found for user {instance.email}.")
            else:
                logger.info(f"User {instance.email} is a client, no Employee record created.")

        except Exception as e:
            logger.error(f"Failed to create profile and/or employee for {instance.email}: {e}")
