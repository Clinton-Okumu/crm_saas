# Generated by Django 5.1.2 on 2024-12-31 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hrm", "0005_remove_employee_user_employee_email_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
