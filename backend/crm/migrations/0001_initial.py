# Generated by Django 5.1.2 on 2024-12-26 17:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Company or customer name', max_length=200)),
                ('email', models.EmailField(blank=True, help_text='Primary email address for the customer', max_length=254)),
                ('phone', models.CharField(blank=True, help_text='Primary phone number', max_length=20)),
                ('website', models.URLField(blank=True, help_text='Company website URL')),
                ('address', models.TextField(blank=True, help_text='Complete address of the customer')),
                ('status', models.CharField(choices=[('lead', 'Lead'), ('customer', 'Customer'), ('inactive', 'Inactive')], default='lead', help_text='Current status of the customer in the sales pipeline', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date and time when the customer was added')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date and time of the last update')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text="Contact's first name", max_length=100)),
                ('last_name', models.CharField(help_text="Contact's last name", max_length=100)),
                ('email', models.EmailField(blank=True, help_text="Contact's email address", max_length=254)),
                ('phone', models.CharField(blank=True, help_text="Contact's phone number", max_length=20)),
                ('position', models.CharField(blank=True, help_text="Contact's job title or position", max_length=100)),
                ('is_primary', models.BooleanField(default=False, help_text='Indicates if this is the primary contact for the customer')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date and time when the contact was added')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date and time of the last update')),
                ('customer', models.ForeignKey(help_text='The customer/company this contact belongs to', on_delete=django.db.models.deletion.CASCADE, to='crm.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Interaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('call', 'Phone Call'), ('email', 'Email'), ('meeting', 'Meeting'), ('note', 'Note')], help_text='The type of interaction', max_length=20)),
                ('notes', models.TextField(help_text='Detailed notes about the interaction')),
                ('date', models.DateTimeField(help_text='Date and time of the interaction')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date and time when this record was created')),
                ('contact', models.ForeignKey(blank=True, help_text='The specific contact person involved (if any)', null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.contact')),
                ('created_by', models.ForeignKey(help_text='User who recorded this interaction', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_interactions', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(help_text='The customer involved in this interaction', on_delete=django.db.models.deletion.CASCADE, to='crm.customer')),
            ],
        ),
    ]
