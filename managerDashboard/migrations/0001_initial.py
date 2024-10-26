# Generated by Django 5.1.2 on 2024-10-26 00:55

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('location', models.CharField(max_length=255)),
                ('entrance_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('image', models.URLField(blank=True, max_length=500, null=True, validators=[django.core.validators.URLValidator()])),
                ('created_by', models.ForeignKey(limit_choices_to={'role': 'EVENT_MANAGER'}, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='main.userprofile')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
    ]
