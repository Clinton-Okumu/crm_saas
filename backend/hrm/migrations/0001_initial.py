# Generated by Django 5.1.2 on 2024-12-31 12:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Employee",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("employee_id", models.CharField(max_length=100, unique=True)),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("phone", models.CharField(blank=True, max_length=20)),
                ("department", models.CharField(blank=True, max_length=100)),
                ("position", models.CharField(blank=True, max_length=100)),
                ("hire_date", models.DateField()),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "Active"), ("inactive", "Inactive")],
                        default="active",
                        max_length=20,
                    ),
                ),
            ],
            options={
                "verbose_name": "employee",
                "verbose_name_plural": "employees",
                "ordering": ["email"],
            },
        ),
        migrations.CreateModel(
            name="LeaveType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("days_allowed", models.PositiveIntegerField()),
                ("is_active", models.BooleanField(default=True)),
                (
                    "max_days_per_year",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Position",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                (
                    "module",
                    models.CharField(
                        choices=[
                            ("hrm", "Human Resources"),
                            ("accounting", "Accounting"),
                            ("project", "Project Management"),
                            ("crm", "Customer Relationship"),
                            ("meeting", "Meeting Management"),
                        ],
                        default="hrm",
                        max_length=20,
                    ),
                ),
                ("description", models.TextField(blank=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Department",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "manager",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="managed_departments",
                        to="hrm.employee",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Goal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("target_date", models.DateField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("in_progress", "In Progress"),
                            ("completed", "Completed"),
                            ("cancelled", "Cancelled"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                (
                    "priority",
                    models.CharField(
                        choices=[
                            ("low", "Low"),
                            ("medium", "Medium"),
                            ("high", "High"),
                        ],
                        default="medium",
                        max_length=20,
                    ),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="hrm.employee"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LeaveRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("reason", models.TextField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("approved", "Approved"),
                            ("rejected", "Rejected"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="hrm.employee"
                    ),
                ),
                (
                    "leave_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="hrm.leavetype"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PayrollRecord",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("salary", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "total_deductions",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("net_salary", models.DecimalField(decimal_places=2, max_digits=10)),
                ("payment_date", models.DateField()),
                ("payment_method", models.CharField(max_length=50)),
                ("remarks", models.TextField(blank=True, null=True)),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="hrm.employee"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PerformanceReview",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("review_period", models.CharField(max_length=50)),
                ("review_date", models.DateField()),
                (
                    "overall_rating",
                    models.PositiveIntegerField(
                        choices=[
                            (1, "Poor"),
                            (2, "Needs Improvement"),
                            (3, "Meets Expectations"),
                            (4, "Exceeds Expectations"),
                            (5, "Outstanding"),
                        ],
                        null=True,
                    ),
                ),
                ("comments", models.TextField(blank=True)),
                ("action_items", models.TextField(blank=True, null=True)),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="hrm.employee"
                    ),
                ),
                (
                    "reviewer",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="reviews_given",
                        to="hrm.employee",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Salary",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("basic_salary", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "bonus",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("effective_date", models.DateField()),
                (
                    "employee",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="hrm.employee"
                    ),
                ),
            ],
        ),
    ]
