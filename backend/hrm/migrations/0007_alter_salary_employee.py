# Generated by Django 5.1.2 on 2025-01-01 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hrm", "0006_employee_is_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="salary",
            name="employee",
            field=models.CharField(max_length=100),
        ),
    ]
