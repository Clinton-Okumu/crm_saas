# hrm/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from .models import Employee
from users.models import CustomUser
from hrm.models import Department, Position
from datetime import date

@receiver(post_save, sender=CustomUser)
def create_employee(sender, instance, created, **kwargs):
    if created:
        try:
            # Define your default department and position
            default_department = Department.objects.first()  # Choose or define default department
            default_position = Position.objects.first()  # Choose or define default position

            if default_department and default_position:
                # Create the Employee record when a CustomUser is created
                Employee.objects.create(
                    user=instance,
                    first_name=instance.first_name,
                    last_name=instance.last_name,
                    email=instance.email,
                    phone=instance.phone,
                    employee_id=f"EMP{instance.id:05d}",  # Generate an employee ID
                    department=default_department,
                    position=default_position,
                    hire_date=date.today(),  # Default hire date
                )
        except ObjectDoesNotExist:
            # Handle the case where department or position doesn't exist
            print("Error: Default department or position not found.")
