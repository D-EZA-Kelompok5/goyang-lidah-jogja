# Generated by Django 5.1.2 on 2024-10-25 09:44

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
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_code', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.URLField(blank=True, max_length=500, null=True, validators=[django.core.validators.URLValidator()])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menus', to='main.restaurant')),
            ],
            options={
                'verbose_name': 'Menu',
                'verbose_name_plural': 'Menus',
                'ordering': ['restaurant', 'menu_code'],
                'unique_together': {('restaurant', 'menu_code')},
            },
        ),
    ]
