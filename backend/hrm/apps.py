from django.apps import AppConfig

class HrmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hrm'  # Replace with your actual app name
    verbose_name = 'Human Resource Management'

    def ready(self):
        import hrm.signals
