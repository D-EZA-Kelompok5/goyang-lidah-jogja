# Generated by Django 5.1.2 on 2024-10-26 11:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0003_remove_menu_restaurant_remove_wishlist_menu_and_more'),
        ('menuResto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlisted_by', to='menuResto.menu')),
                ('user', models.ForeignKey(limit_choices_to={'role': 'CUSTOMER'}, on_delete=django.db.models.deletion.CASCADE, related_name='wishlists', to='main.userprofile')),
            ],
            options={
                'verbose_name': 'Wishlist',
                'verbose_name_plural': 'Wishlists',
            },
        ),
    ]
