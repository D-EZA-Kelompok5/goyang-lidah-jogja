# Generated by Django 5.1.3 on 2024-12-22 03:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ulasGoyangan', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='last_edited',
            new_name='updated_at',
        ),
    ]
