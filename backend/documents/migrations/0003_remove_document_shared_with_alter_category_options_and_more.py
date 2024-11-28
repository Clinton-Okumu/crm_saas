# Generated by Django 5.1.2 on 2024-11-27 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_alter_documentshare_permission_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='shared_with',
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='document',
            options={'ordering': ['-updated_at']},
        ),
        migrations.RemoveField(
            model_name='document',
            name='last_accessed',
        ),
        migrations.DeleteModel(
            name='DocumentShare',
        ),
    ]