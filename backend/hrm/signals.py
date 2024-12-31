from django.db import transaction
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps
from users.models import CustomUser

@receiver(post_migrate)
def create_initial_positions(sender, **kwargs):
    # Only run for our app
    if kwargs.get('app_config').name != 'hrm':  # Replace with your actual app name
        return
        
    Position = apps.get_model('hrm', 'Position')
    
    # Map roles to their corresponding modules and descriptions
    position_data = [
        # System Positions
        {
            'title': CustomUser.Role.SUPER_ADMIN.label,
            'module': CustomUser.Module.HRM,
            'description': 'System administrator with full access'
        },
        
        # HR Module Positions
        {
            'title': CustomUser.Role.HR_ADMIN.label,
            'module': CustomUser.Module.HRM,
            'description': 'HR administrator with full HR module access'
        },
        {
            'title': CustomUser.Role.HR_MANAGER.label,
            'module': CustomUser.Module.HRM,
            'description': 'HR manager responsible for HR operations'
        },
        {
            'title': CustomUser.Role.HR_STAFF.label,
            'module': CustomUser.Module.HRM,
            'description': 'HR staff member'
        },
        
        # Accounting Module Positions
        {
            'title': CustomUser.Role.ACCOUNTING_ADMIN.label,
            'module': CustomUser.Module.ACCOUNTING,
            'description': 'Accounting administrator with full accounting module access'
        },
        {
            'title': CustomUser.Role.ACCOUNTANT.label,
            'module': CustomUser.Module.ACCOUNTING,
            'description': 'Staff accountant'
        },
        
        # Project Module Positions
        {
            'title': CustomUser.Role.PROJECT_ADMIN.label,
            'module': CustomUser.Module.PROJECT,
            'description': 'Project administrator with full project module access'
        },
        {
            'title': CustomUser.Role.PROJECT_MANAGER.label,
            'module': CustomUser.Module.PROJECT,
            'description': 'Project manager responsible for project operations'
        },
        {
            'title': CustomUser.Role.PROJECT_MEMBER.label,
            'module': CustomUser.Module.PROJECT,
            'description': 'Project team member'
        },
        
        # CRM Module Positions
        {
            'title': CustomUser.Role.CRM_ADMIN.label,
            'module': CustomUser.Module.CRM,
            'description': 'CRM administrator with full CRM module access'
        },
        {
            'title': CustomUser.Role.CRM_MANAGER.label,
            'module': CustomUser.Module.CRM,
            'description': 'CRM manager responsible for customer relations'
        },
        {
            'title': CustomUser.Role.SALES_REP.label,
            'module': CustomUser.Module.CRM,
            'description': 'Sales representative'
        },
        
        # Client Position
        {
            'title': CustomUser.Role.CLIENT.label,
            'module': CustomUser.Module.PROJECT,  # Clients primarily interact with projects
            'description': 'External client user'
        }
    ]

    with transaction.atomic():
        for pos_data in position_data:
            Position.objects.get_or_create(
                title=pos_data['title'],
                module=pos_data['module'],
                defaults={
                    'description': pos_data['description'],
                    'is_active': True
                }
            )
